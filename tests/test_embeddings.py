from utils.embeddings import get_embedding

def test_get_embedding():
    emb = get_embedding('hello world')
    assert isinstance(emb, list)
    assert len(emb) > 0
