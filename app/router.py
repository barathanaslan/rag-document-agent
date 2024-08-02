# app/router.py
import json
import logging
from fastapi import APIRouter, Body, Request
from fastapi.templating import Jinja2Templates
from qdrant_client import QdrantClient, models
from langchain.prompts import ChatPromptTemplate

from app.embedding import embed_text, upload_documents
from app.memory import memory, llm_model
from app.utils import get_text_from_directory, count_tokens
from app.config import qdrant_client, collection_name, tokenizer, vector_size

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def on_startup():
    try:
        qdrant_client.get_collection(collection_name)
        logging.warning(f"Collection {collection_name} already exists.")
    except ValueError:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )
        logging.info(f"Collection {collection_name} created.")

    # Check if the collection has any records
    response = qdrant_client.count(collection_name)
    if response.count == 0:
        texts = get_text_from_directory("auto_files")
        sentence_chunk_map = upload_documents(texts, tokenizer)
        with open('sentence_chunk_map.json', 'w') as f:
            json.dump(sentence_chunk_map, f)

@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/query")
async def query_endpoint(query: dict = Body(...)):
    query_text = query.get("query_text")
    query_embedding = embed_text([query_text])[0]

    try:
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=3
        )

        if search_results:
            with open('sentence_chunk_map.json', 'r') as f:
                sentence_chunk_map = json.load(f)
            context_chunks = set()
            for hit in search_results:
                sentence_id = hit.id
                context_chunks.add(sentence_chunk_map[sentence_id])
            
            context_text = "\n\n---\n\n".join(context_chunks)
            logging.info("Found relevant chunks:")
            for idx, chunk in enumerate(context_chunks):
                logging.info(f"Chunk {idx+1}: {chunk}")
        else:
            context_text = "No relevant information found in document."
            logging.warning("No relevant information found in document.")

        # Update prompt template to include memory
        PROMPT_TEMPLATE = """
        You are a concise AI Assistant working for Barathan. Your task is to provide accurate and direct answers based on the provided context and previous conversation. Avoid explaining your reasoning.

        Previous conversation:
        {history}
        ---
        Context:
        {context}
        ---
        Question: {question}
        ---
        Answer directly, only if the information is found within the provided context and conversation history. If the information is not available, respond with: "I cannot answer based on the provided context." 
        """
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
            history=memory.load_memory_variables({}),
            context=context_text,
            question=query_text
        )

        response_text = llm_model(prompt)
        
        # Save the interaction to memory
        memory.save_context({"input": query_text}, {"output": response_text})

        total_prompt_tokens = count_tokens(prompt, tokenizer)
        total_response_tokens = count_tokens(response_text, tokenizer)
        total_tokens = total_prompt_tokens + total_response_tokens
        logging.warning(f"Total tokens used for query: {total_tokens}")

        return {"response": response_text}
    except ValueError as e:
        logging.error(f"Error during query: {e}")
        return {"response": "An error occurred while processing your query."}
