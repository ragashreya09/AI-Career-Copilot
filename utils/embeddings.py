import os, openai
from typing import List
MODEL = os.getenv('OPENAI_EMBEDDING_MODEL','text-embedding-3-small')

def get_embedding(text: str):
    text = text[:8192]
    resp = openai.Embedding.create(model=MODEL, input=text)
    return resp['data'][0]['embedding']

def embed_texts(texts):
    resp = openai.Embedding.create(model=MODEL, input=texts)
    return [d['embedding'] for d in resp['data']]
