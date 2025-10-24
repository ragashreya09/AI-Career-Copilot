# AI Career Copilot (Full)

This is the full version of the AI Career Copilot project with:
- FastAPI backend that analyzes resumes and job descriptions using OpenAI LLM and embeddings
- Streamlit frontend for uploading resume/JD and receiving feedback
- Utility modules for text extraction, embeddings, and optional Pinecone integration

## Quick start
1. Create a virtualenv: `python3 -m venv .venv && source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your `OPENAI_API_KEY` (and Pinecone keys if you use Pinecone).
4. Start backend: `uvicorn backend.app:app --reload --port 8000`
5. Start frontend: `streamlit run frontend/streamlit_app.py`
