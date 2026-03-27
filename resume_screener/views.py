import os
from typing import Any, cast

import fitz  # PyMuPDF
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename

from django.shortcuts import render
from django.conf import settings


# ── Upload folder (inside resume_screener app directory) ──
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'resume_screener', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ── PDF text extraction ──
def extract_text_from_pdf(file_path):
    text_parts = []
    pdf = fitz.open(file_path)
    for page in pdf:
        page_text = page.get_text("text")
        text_parts.append(page_text if isinstance(page_text, str) else "")
    return " ".join(text_parts)


# ── DOCX text extraction ──
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])


# ── Read resume ──
def read_resume(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return ""


# ── TF-IDF cosine similarity ──
def get_similarity(job_desc, resume_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([job_desc, resume_text])
    dense_vectors = cast(Any, vectors).toarray()
    score = cosine_similarity(dense_vectors[0:1], dense_vectors[1:2])
    return round(float(score[0][0]) * 100, 2)


# ── Main view ──
def screener(request):
    results = []

    if request.method == "POST":
        job_desc = request.POST.get("job_description", "").strip()
        files = request.FILES.getlist("resumes")

        for file in files:
            if file:
                original_name = file.name or ""
                safe_name = secure_filename(original_name)
                if not safe_name:
                    continue

                file_path = os.path.join(UPLOAD_DIR, safe_name)
                with open(file_path, 'wb+') as dest:
                    for chunk in file.chunks():
                        dest.write(chunk)

                resume_text = read_resume(file_path)
                score = get_similarity(job_desc, resume_text)

                results.append({
                    "name": safe_name,
                    "score": score,
                })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

    return render(request, 'resume_screener/screener.html', {'results': results})
