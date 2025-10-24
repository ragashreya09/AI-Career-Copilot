import os
try:
    import pinecone
except Exception:
    pinecone = None

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENVIRONMENT')
INDEX_NAME = os.getenv('PINECONE_INDEX','ai-career-copilot')

def init_pinecone():
    if pinecone is None:
        raise RuntimeError('pinecone client not installed')
    if not pinecone.is_initialized():
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

def upsert_job_embedding(job_description: str, namespace: str = 'jobs'):
    try:
        init_pinecone()
        from utils.embeddings import get_embedding
        emb = get_embedding(job_description)
        idx = pinecone.Index(INDEX_NAME)
        idx.upsert([(f'job-{hash(job_description)}', emb)], namespace=namespace)
    except Exception as e:
        print('pinecone upsert failed:', e)

def query_similar_jobs(texts: list, top_k: int = 3, namespace: str = 'jobs'):
    init_pinecone()
    from utils.embeddings import embed_texts
    embs = embed_texts(texts)
    idx = pinecone.Index(INDEX_NAME)
    results = idx.query(embs[0], top_k=top_k, namespace=namespace)
    return results['matches']
