# app/embedding.py
import uuid
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from qdrant_client import models, QdrantClient

from app.config import model, qdrant_client, collection_name, vector_size
from app.utils import count_tokens, split_text_into_chunks, split_chunks_into_sentences

import logging

def embed_text(text_list: List[str]) -> List[List[float]]:
    if not text_list:
        return []
    return model.encode(text_list).tolist()

def upload_documents(texts: List[str], tokenizer) -> Dict[str, str]:
    all_records = []
    sentence_chunk_map = {}
    total_tokens = 0
    for idx, text in enumerate(texts):
        chunks = split_text_into_chunks(text)
        for chunk_idx, chunk in enumerate(chunks):
            sentences = split_chunks_into_sentences([chunk])
            if not sentences:
                continue  # Skip if there are no sentences
            embeddings = embed_text(sentences)
            for sentence, embedding in zip(sentences, embeddings):
                record_id = str(uuid.uuid4())
                record = models.Record(
                    id=record_id,
                    vector=embedding,
                    payload={"text": sentence}
                )
                all_records.append(record)
                sentence_chunk_map[record_id] = chunk
                total_tokens += count_tokens(sentence, tokenizer)
    logging.info(f"Total tokens used for document upload: {total_tokens}")
    qdrant_client.upload_records(collection_name=collection_name, records=all_records)
    logging.info(f"Uploaded {len(all_records)} records to the collection.")
    return sentence_chunk_map
