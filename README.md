# ResumeIQ — Explainable Resume–Job Matcher

ResumeIQ is an interactive Streamlit application that compares a candidate resume with a job description and produces an explainable alignment report. It combines canonical skill extraction, TF-IDF text similarity and experience evidence into a transparent score. The goal is to help candidates tailor applications while keeping the result interpretable rather than presenting an opaque prediction.

## Why this project matters

Recruiters and candidates often need to compare a resume against a role quickly. ResumeIQ demonstrates a complete applied machine-learning workflow: document ingestion, text processing, feature engineering, similarity scoring, explainable recommendations, interactive UI and automated testing. The application is intentionally designed as an assistive tool; it does not make hiring decisions and should not be used as an automated screening system.

## Features

| Capability | Description |
|---|---|
| Multi-format ingestion | Reads PDF, DOCX, TXT and Markdown files. |
| Hybrid matching | Combines skill coverage, TF-IDF similarity and experience signals. |
| Explainability | Shows matched skills, missing skills, score components and recommendations. |
| Resume quality signals | Detects the presence of email, phone, LinkedIn and GitHub fields without persisting their values. |
| Interactive dashboard | Streamlit interface with score cards, charts and expandable methodology. |
| Testing | Pytest coverage for aliases, scoring, missing skills and section parsing. |

## Scoring methodology

The overall score is an assistive signal calculated as follows:

```text
Overall score = 0.55 × skill coverage
              + 0.30 × TF-IDF text similarity
              + 0.15 × experience evidence
```

Skill coverage is the proportion of job-description skills detected in the resume. Text similarity uses a TF-IDF vectorizer with unigram and bigram features. Experience evidence compares explicit year-of-experience signals where available. The application exposes each component so that a user can understand why the score changes.

## Project structure

```text
resume_job_matcher/
├── app/
│   └── main.py                 # Streamlit entry point
├── src/
│   ├── matcher.py              # Skill taxonomy and scoring engine
│   ├── parser.py               # PDF, DOCX and text parsing utilities
│   └── __init__.py
├── tests/
│   └── test_matcher.py         # Automated tests
├── docs/
│   └── PROJECT_REPORT.md       # Project report
├── assets/
│   └── .gitkeep                # Screenshots and diagrams go here
├── .streamlit/config.toml
├── requirements.txt
└── README.md
```

## Setup

Use Python 3.10 or newer. From the project directory, create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows Command Prompt
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app/main.py
```

The browser will open the Streamlit interface. If it does not open automatically, visit the URL printed in the terminal, normally `http://localhost:8501`.

For a lightweight first run, install all packages except the optional `sentence-transformers` package. The current engine does not require a downloaded transformer model; it uses a deterministic TF-IDF fallback so that the application remains fast and reproducible.

## Usage

Upload a resume in PDF, DOCX, TXT or MD format, paste the complete job description, and select **Analyze match**. The report includes an overall match percentage, component scores, matched skills, skills to strengthen, resume completeness signals and tailored recommendations. Use the sidebar sample data to test the application before adding a personal document.

## Responsible-use note

Resume data may contain sensitive personal information. In this demo, documents are read in memory and are not saved by the application. Do not upload private documents to an untrusted deployment. The score is not a measure of a person's ability, and it should never be used as the sole basis for employment decisions.

## Future improvements

The next portfolio iteration can add sentence-transformer embeddings, a configurable skill taxonomy, a labelled evaluation dataset, recruiter-facing batch analysis, a RAG assistant for resume improvement and an agentic workflow that converts missing skills into a personalised learning plan. Those additions should be evaluated separately from the baseline so that improvements remain measurable.

## Portfolio bullet

> Built ResumeIQ, an explainable Streamlit resume–job matching application that parses PDF/DOCX/TXT files and combines skill coverage, TF-IDF similarity and experience evidence to generate actionable tailoring recommendations.
