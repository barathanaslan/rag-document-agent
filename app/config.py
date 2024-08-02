# app/config.py
import os
from qdrant_client import QdrantClient
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Initialize Qdrant client
current_directory = os.getcwd()
qdrant_client = QdrantClient(path=os.path.join(current_directory, "db"))

# Define collection parameters
collection_name = "sentence_vector_db"
vector_size = model.get_sentence_embedding_dimension()
