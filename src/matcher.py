"""Hybrid matching engine combining skills, TF-IDF and experience signals."""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "python": ("python",),
    "sql": ("sql", "mysql", "postgresql", "postgres"),
    "pandas": ("pandas",),
    "numpy": ("numpy",),
    "scikit-learn": ("scikit-learn", "sklearn"),
    "tensorflow": ("tensorflow", "keras"),
    "pytorch": ("pytorch", "torch"),
    "machine learning": ("machine learning", "ml"),
    "deep learning": ("deep learning", "dl"),
    "natural language processing": ("natural language processing", "nlp"),
    "computer vision": ("computer vision", "opencv"),
    "statistics": ("statistics", "statistical analysis"),
    "data analysis": ("data analysis", "data analytics"),
    "data visualization": ("data visualization", "tableau", "power bi", "powerbi"),
    "feature engineering": ("feature engineering",),
    "model deployment": ("model deployment", "deployment", "mlops"),
    "docker": ("docker",),
    "kubernetes": ("kubernetes", "k8s"),
    "aws": ("aws", "amazon web services"),
    "azure": ("azure",),
    "gcp": ("gcp", "google cloud"),
    "git": ("git", "github", "gitlab"),
    "streamlit": ("streamlit",),
    "fastapi": ("fastapi",),
    "flask": ("flask",),
    "airflow": ("airflow",),
    "spark": ("spark", "pyspark"),
    "llm": ("llm", "large language model", "large language models"),
    "generative ai": ("generative ai", "genai", "gen ai"),
    "prompt engineering": ("prompt engineering",),
    "rag": ("rag", "retrieval augmented generation", "retrieval-augmented generation"),
    "langchain": ("langchain",),
    "langgraph": ("langgraph",),
    "vector database": ("vector database", "vector db", "faiss", "chroma", "pinecone"),
    "transformers": ("transformers", "huggingface", "hugging face"),
    "reinforcement learning": ("reinforcement learning", "rl", "q-learning", "dqn"),
    "react": ("react", "react.js", "reactjs"),
    "javascript": ("javascript", "js"),
    "typescript": ("typescript", "ts"),
    "communication": ("communication", "presentation", "stakeholder"),
}


@dataclass
class MatchResult:
    overall_score: float
    skill_score: float
    semantic_score: float
    evidence_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    required_skills: list[str]
    recommendations: list[str]
    keyword_frequency: dict[str, int]

    def to_dict(self) -> dict:
        return asdict(self)


def _contains_alias(text: str, alias: str) -> bool:
    escaped = re.escape(alias.lower())
    return bool(re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", text.lower()))


def extract_skills(text: str) -> list[str]:
    """Extract canonical skills from free text using alias matching."""
    lowered = text.lower()
    found = [canonical for canonical, aliases in SKILL_ALIASES.items() if any(_contains_alias(lowered, alias) for alias in aliases)]
    return sorted(found)


def _tfidf_score(resume: str, job: str) -> float:
    if not resume.strip() or not job.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    try:
        matrix = vectorizer.fit_transform([resume, job])
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        return 0.0


def _experience_score(resume: str, job: str) -> float:
    resume_years = [float(value) for value in re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*years?", resume.lower())]
    job_years = [float(value) for value in re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*years?", job.lower())]
    if not job_years:
        return 0.75
    if not resume_years:
        return 0.25
    return min(max(max(resume_years) / max(job_years), 0.0), 1.0)


def _recommendations(missing: Iterable[str], semantic_score: float, evidence_score: float) -> list[str]:
    missing_list = list(missing)
    recommendations: list[str] = []
    if missing_list:
        recommendations.append("Add evidence for these job skills where truthful: " + ", ".join(missing_list[:8]) + ".")
    if evidence_score < 0.55:
        recommendations.append("Rewrite project and experience bullets using measurable outcomes, tools and business impact.")
    if semantic_score < 0.45:
        recommendations.append("Mirror the job description's relevant terminology naturally in your summary and skills sections.")
    if not recommendations:
        recommendations.append("Strong alignment. Tailor the first three experience bullets to the most important role outcomes.")
    return recommendations


def match_resume_to_job(resume_text: str, job_text: str) -> MatchResult:
    resume_text = resume_text.strip()
    job_text = job_text.strip()
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_text)
    matched = sorted(set(resume_skills) & set(required_skills))
    missing = sorted(set(required_skills) - set(resume_skills))
    skill_score = len(matched) / len(required_skills) if required_skills else 0.0
    semantic_score = _tfidf_score(resume_text, job_text)
    evidence_score = _experience_score(resume_text, job_text)
    overall = float(np.clip((0.55 * skill_score) + (0.30 * semantic_score) + (0.15 * evidence_score), 0.0, 1.0))
    keyword_frequency = {skill: sum(_contains_alias(resume_text, alias) for alias in aliases) for skill, aliases in SKILL_ALIASES.items() if any(_contains_alias(job_text, alias) for alias in aliases)}
    return MatchResult(
        overall_score=round(overall * 100, 1),
        skill_score=round(skill_score * 100, 1),
        semantic_score=round(semantic_score * 100, 1),
        evidence_score=round(evidence_score * 100, 1),
        matched_skills=matched,
        missing_skills=missing,
        resume_skills=resume_skills,
        required_skills=required_skills,
        recommendations=_recommendations(missing, semantic_score, evidence_score),
        keyword_frequency=keyword_frequency,
    )
