import os
from PyPDF2 import PdfReader
import docx

def extract_text_from_file(path: str, filename: str = None) -> str:
    filename = filename or path
    lower = filename.lower()
    if lower.endswith('.pdf'):
        reader = PdfReader(path)
        text = []
        for p in reader.pages:
            text.append(p.extract_text() or '')
        return '\n'.join(text)
    elif lower.endswith('.docx') or lower.endswith('.doc'):
        doc = docx.Document(path)
        return '\n'.join(p.text for p in doc.paragraphs)
    else:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
