import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.matcher import extract_skills, match_resume_to_job
from src.parser import clean_text, split_sections


def test_extract_skills_canonicalizes_aliases():
    skills = extract_skills("Python, sklearn, NLP, Docker and LangGraph")
    assert "python" in skills
    assert "scikit-learn" in skills
    assert "natural language processing" in skills
    assert "docker" in skills
    assert "langgraph" in skills


def test_matcher_returns_high_score_for_aligned_resume():
    resume = "Python developer with 2 years experience in SQL, pandas, scikit-learn, machine learning and Git."
    job = "Looking for Python, SQL, pandas, scikit-learn, machine learning and Git. 1 year experience required."
    result = match_resume_to_job(resume, job)
    assert result.overall_score > 70
    assert "python" in result.matched_skills
    assert not result.missing_skills


def test_matcher_identifies_missing_skills():
    result = match_resume_to_job("Python and pandas developer", "Need Python, pandas, Docker and AWS")
    assert "docker" in result.missing_skills
    assert "aws" in result.missing_skills


def test_parser_sections_and_cleaning():
    text = "SUMMARY\nPython developer\n\n\nSKILLS\nPython, SQL"
    cleaned = clean_text(text)
    sections = split_sections(cleaned)
    assert sections["summary"] == "Python developer"
    assert "Python" in sections["skills"]
