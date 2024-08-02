# app/utils.py
import os
import re
from typing import List
import logging

def count_tokens(text: str, tokenizer) -> int:
    return len(tokenizer.encode(text))

def get_text_from_directory(directory_path: str) -> List[str]:
    texts = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8") as file:
                texts.append(file.read())
    return texts

def split_text_into_chunks(text: str) -> List[str]:
    return text.split("***")

def split_chunks_into_sentences(chunks: List[str]) -> List[str]:
    sentences = []
    for chunk in chunks:
        sentences.extend(re.split(r'\.|\?|:|\*{3}', chunk))
    return [sentence.strip() for sentence in sentences if sentence.strip()]
