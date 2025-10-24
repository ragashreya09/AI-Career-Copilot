from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, tempfile
from utils.resume_parser import extract_text_from_file
from utils.embeddings import get_embedding, embed_texts
from utils.pinecone_client import upsert_job_embedding, query_similar_jobs
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = FastAPI(title="AI Career Copilot Backend")

class JDAnalysisRequest(BaseModel):
    job_description: str

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None

@app.post('/analyze_resume')
async def analyze_resume(payload: ResumeAnalysisRequest):
    resume_text = payload.resume_text
    jd = payload.job_description
    result = {}
    if jd:
        try:
            sims = query_similar_jobs([resume_text], top_k=3)
            result['pinecone_similar_jobs'] = sims
        except Exception as e:
            r_emb = get_embedding(resume_text)
            jd_emb = get_embedding(jd)
            sim = sum(a*b for a,b in zip(r_emb, jd_emb))
            result['embedding_similarity_dot'] = sim

    prompt = f"You are a career assistant. Given this resume text:\n\n{resume_text}\n\n"
    if jd:
        prompt += f"And this job description:\n\n{jd}\n\n"
    prompt += "Provide: 1) ATS-friendly title and 2) Top 8 resume bullet suggestions to improve match, and 3) Skills gap list. Respond as JSON object keys: title, bullets, gaps."

    completion = openai.ChatCompletion.create(
        model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),
        messages=[{"role":"user","content":prompt}],
        max_tokens=600
    )
    content = completion['choices'][0]['message']['content']
    result['llm_feedback'] = content
    return result

@app.post('/analyze_job')
async def analyze_job(req: JDAnalysisRequest):
    jd = req.job_description
    upsert_job_embedding(jd)
    return {"status":"ok","message":"JD embedded (or stored)"}

@app.post('/upload_resume_file')
async def upload_resume_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(content)
        tmp.flush()
        txt = extract_text_from_file(tmp.name, filename=file.filename)
        return {"text": txt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
