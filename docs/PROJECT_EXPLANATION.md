# ResumeIQ — Simple Project Explanation for Presentation and Viva

## 1. One-line introduction

ResumeIQ is an explainable web application that compares a candidate's resume with a job description and shows how well the resume matches the role, which skills are already present, which skills are missing, and how the candidate can improve the resume.

## 2. Problem statement

Candidates often use the same resume for different jobs. Every job description has different required skills and terminology. Manually comparing a resume with every job is slow and it is easy to miss important requirements. ResumeIQ automates this first comparison and gives a transparent report.

## 3. Main objectives

The project accepts resumes in PDF, DOCX, TXT and Markdown formats. It extracts the text, detects relevant skills, compares the resume with the job description, calculates an explainable score, and displays practical recommendations in a browser-based Streamlit interface.

## 4. Complete workflow

```text
Upload resume and job description
              ↓
Extract text from PDF, DOCX or TXT
              ↓
Clean and normalise the text
              ↓
Detect canonical skills and aliases
              ↓
Calculate skill coverage
              ↓
Calculate TF-IDF text similarity
              ↓
Estimate experience evidence
              ↓
Combine the three signals into one score
              ↓
Display score, matched skills, missing skills and recommendations
```

### Step 1 — Input

The user uploads a resume and enters or uploads a job description. The application processes the files in memory for this demo and does not intentionally save the uploaded personal documents.

### Step 2 — Document parsing

PDF text is extracted with `pypdf`, and DOCX text is extracted with `python-docx`. Plain text and Markdown files are decoded as UTF-8. Whitespace is normalised so that the matching engine receives clean text.

### Step 3 — Skill extraction

The project contains a canonical skill taxonomy. Different names can map to one canonical skill. For example, `sklearn` maps to `scikit-learn`, and `genai` maps to `generative ai`. Boundary-aware matching reduces accidental matches inside unrelated words.

### Step 4 — Skill coverage

The system compares skills detected in the resume with skills detected in the job description.

```text
Skill coverage = matched job skills / total detected job skills
```

This tells the candidate which explicit requirements are already represented in the resume.

### Step 5 — Text similarity

The system uses TF-IDF with one-word and two-word features. TF-IDF gives higher importance to words that are meaningful in the documents and cosine similarity measures how similar the resume and job-description vectors are. This is a classical machine-learning baseline, not a large language model.

### Step 6 — Experience evidence

If the text contains expressions such as `2 years experience`, the system compares the resume evidence with an explicit experience requirement in the job description. If the job does not state years, a neutral evidence score is used.

### Step 7 — Final score

The final score is a weighted combination of three interpretable signals:

| Signal | Weight | Meaning |
|---|---:|---|
| Skill coverage | 55% | How many detected role skills are present in the resume. |
| TF-IDF similarity | 30% | How much important vocabulary overlaps. |
| Experience evidence | 15% | Whether explicit experience signals align. |

```text
Overall score = 0.55 × skill coverage
              + 0.30 × TF-IDF similarity
              + 0.15 × experience evidence
```

### Step 8 — Result

The Streamlit dashboard displays the overall score, score breakdown, matched skills, missing skills, resume completeness signals and recommendations. The score is an assistive signal and is not a hiring decision.

## 5. Tools and technologies

| Tool | Why it is used |
|---|---|
| Python | Main programming language. |
| Streamlit | Builds the interactive browser-based web application. |
| pandas | Organises section-level and result data. |
| NumPy | Clips and handles numerical score calculations. |
| scikit-learn | TF-IDF vectorisation and cosine similarity. |
| pypdf | Extracts text from PDF resumes. |
| python-docx | Extracts text from DOCX resumes. |
| Plotly | Displays the score-breakdown chart. |
| pytest | Tests the parser and matching engine. |
| Git/GitHub | Version control, portfolio publishing and collaboration. |

## 6. Why classical ML instead of ChatGPT?

The first version uses a deterministic classical-ML baseline because it is fast, reproducible, inexpensive and easy to explain in a presentation. A black-box LLM score would be difficult to validate. The system can later add sentence embeddings or an LLM-based resume coach, but those additions should be evaluated against this baseline instead of replacing it without measurement.

## 7. Applications

ResumeIQ can be used by students to tailor resumes for internships, by job seekers to identify missing keywords, by career cells to teach resume customisation, and by recruiters as a preliminary review aid. It should not automatically reject or rank people for employment, because resume text cannot fully represent a person's ability or potential.

## 8. Limitations

The skill taxonomy cannot know every possible synonym. TF-IDF mainly measures vocabulary overlap and may miss deeper semantic similarity. Scanned PDFs need OCR, which is not included in this baseline. The experience heuristic only understands explicit year expressions. The system also cannot verify whether a resume claim is true.

## 9. Future improvements

The next version can add sentence-transformer embeddings, OCR, configurable skill taxonomies, a labelled resume–job evaluation dataset, resume improvement suggestions using an LLM, a RAG-based career assistant and an agentic learning-plan generator. Each improvement should be tested against the current baseline.

## 10. Common viva questions and short answers

### What is the main problem solved by the project?

It reduces the time needed to compare a resume with a job description and provides an explainable list of alignment areas and skill gaps.

### Why did you use TF-IDF?

TF-IDF is a strong, fast and interpretable baseline for text similarity. It does not require model training or an external API, so results are reproducible.

### What is cosine similarity?

Cosine similarity measures the angle between two document vectors. A value closer to one means the documents have more similar feature direction, while a value closer to zero means less similarity.

### Why are the weights 55%, 30% and 15%?

Skill coverage is the most direct signal for a job match, so it receives the largest weight. Text similarity provides supporting evidence, and experience evidence is useful but depends on explicit year expressions. These weights are a baseline and should be tuned using labelled evaluation data.

### Is the score an accuracy value?

No. It is an explainable alignment score, not accuracy and not a hiring recommendation. Accuracy would require labelled ground-truth examples and a defined prediction task.

### What happens if a PDF is scanned?

A scanned PDF may not contain selectable text, so the current parser may extract little or no text. OCR can be added as a future improvement.

### How did you test the project?

Pytest tests skill aliases, high-alignment matching, missing-skill detection, text cleaning and section parsing. The tests are in `tests/test_matcher.py`.

### How would you improve the project for production?

I would add a labelled evaluation dataset, semantic embeddings, OCR, stronger privacy controls, configurable taxonomies, monitoring, authentication and a human-review workflow.

### What is the difference between this and an LLM project?

ResumeIQ is the explainable classical-ML baseline. An LLM project would generate or summarise language, while this project focuses on deterministic matching and measurable signals. The two can be combined later in a RAG-based resume coach.

## 11. Two-minute presentation script

“ResumeIQ is an explainable Streamlit application that compares a resume with a target job description. The user uploads a PDF, DOCX or text resume. The parser extracts and cleans the text, the skill extractor maps aliases to canonical skills, and the matching engine calculates three signals: skill coverage, TF-IDF text similarity and experience evidence. These signals are combined into a weighted score, and the dashboard shows matched skills, missing skills and practical recommendations. I chose a classical ML baseline because it is fast, reproducible and easy to explain. The project is modular, tested with pytest, documented on GitHub and ready to extend with embeddings, RAG and an LLM career coach.”
