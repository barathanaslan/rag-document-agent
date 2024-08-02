
# Local Chatbot Agent

This project is a local chatbot agent designed to answer questions based on a set of documents. It uses Qdrant for vector storage and retrieval, and LangChain for language model interaction and memory.

**This was the internship project assigned to me while working at Fimple in the summer of 2024.**

## Unique Approach

### Sentence-Level Encoding

The main and possibly the only difference of this Retrieval-Augmented Generation (RAG) model from other models available on GitHub or elsewhere is its unique approach to encoding and matching text. Instead of directly vectorizing chunks of text, this model encodes each sentence within the chunks individually. The user query is then matched with each sentence in the text rather than with the entire chunk.

#### Performance Difference

- **Chunk-Level Encoding**: Traditional RAG models typically encode larger chunks of text and match the user query with these chunks. While this approach can be faster due to fewer vectors to compare, it often results in less precise matching. This is because the relevant information might be diluted within a larger chunk, reducing the accuracy of the retrieval.

- **Sentence-Level Encoding**: By encoding each sentence individually, our approach increases the granularity of the vector comparisons. This leads to more accurate and relevant matches, as the user query is compared directly with smaller, more precise units of text. Although this method can be more computationally intensive and might require more storage for the increased number of vectors, the improvement in accuracy and relevance of the retrieved information is significant.

## Project Structure

```
local_chatbot_agent/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── utils.py
│   ├── embedding.py
│   ├── memory.py
│   ├── router.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   └── index.html
│
├── auto_files/
│   └── (your text files)
│
├── sentence_chunk_map.json
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Create a directory named `auto_files` and add your text documents there.

**Note**: The `auto_files` directory should contain the scraped or retrieved text files. For this project, web data was scraped and used, but due to data privacy concerns, I am unable to share the original document text. Text files should be separated by "***" to indicate different chunks. Users who want to use this code should either format their text files in the same way or modify the relevant part of the code (utils.py). The GitHub version of this project contains synthetically generated example text files created to mimic the structure of the original ones.

## Running the Application

To start the FastAPI application, run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at `http://0.0.0.0:8000`.

## Usage

- Access the root endpoint (`/`) to view the index page.
- Use the `/query` endpoint to submit a query and receive a response based on the provided documents.

## Technologies Used

- **Sentence Transformer Model**: `all-MiniLM-L6-v2` for encoding sentences into vectors.
- **Language Model**: `llama3` for generating responses based on retrieved context, providing a relatively low GPU load and moderate to high context limit in the given use case.
- **Vector Database**: Qdrant for storing and retrieving sentence embeddings.
- **Frameworks**: FastAPI for the web server, LangChain for memory management.

## Notes

- The application uses Qdrant for vector storage and retrieval.
- The documents are split into chunks and sentences for better retrieval accuracy.
- Conversation history is managed using LangChain's `ConversationSummaryBufferMemory`.

**Note**: In the creation of this project, ChatGPT, Gemini, and Claude were used in several steps.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
