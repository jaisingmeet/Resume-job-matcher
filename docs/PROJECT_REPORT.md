# ResumeIQ Project Report

## Abstract

ResumeIQ is an explainable resume-to-job matching web application built with Python and Streamlit. It accepts a resume and a job description, extracts text from common document formats, identifies relevant technical and professional skills, calculates text similarity and experience evidence, and presents an actionable alignment report. The project focuses on applied machine learning engineering: a reproducible baseline, transparent features, usable interface and clear limitations.

## 1. Problem statement

Candidates frequently submit a generic resume for multiple roles, even though each job description prioritises a different combination of skills and responsibilities. A useful tool should identify the overlap between a resume and a role, highlight gaps that the candidate can address truthfully, and explain how its score was produced. ResumeIQ addresses this need as a decision-support application rather than an automated hiring system.

## 2. Objectives

The project has four objectives. First, it should accept common resume formats with minimal friction. Second, it should produce a reproducible match score using understandable signals. Third, it should translate the analysis into practical recommendations. Fourth, it should demonstrate software-engineering habits such as modular code, testing, documentation and a deployable interface.

## 3. System architecture

```text
Resume PDF/DOCX/TXT ──┐
                      ├── Parser ──> Normalised text ──> Skill extractor ──┐
Job description ──────┘                                                   │
                                                                          ├── Hybrid scorer ──> Report UI
Normalised text ───────────────> TF-IDF similarity ───────────────────────┤
Explicit years of experience ─> Evidence signal ─────────────────────────┘
```

The parser converts each input into normalised text. The matcher then applies a curated canonical skill taxonomy, TF-IDF vectorisation with unigram and bigram features, and a lightweight experience heuristic. Streamlit renders the outputs as score cards, a score-breakdown chart, skill tags and recommendations.

## 4. Methodology

### 4.1 Document processing

PDF files are read with `pypdf`, DOCX files with `python-docx`, and text files with UTF-8 decoding. Whitespace is normalised while paragraph boundaries are preserved. The parser also performs best-effort section detection for summary, experience, education, skills, projects and certification headings.

### 4.2 Skill extraction

The application uses a canonical taxonomy with aliases. For example, `sklearn` maps to `scikit-learn`, while `genai` maps to `generative ai`. Boundary-aware regular expressions reduce accidental substring matches. The taxonomy covers core Python/ML skills, cloud and deployment tools, GenAI technologies, web frameworks and selected communication terms. A production deployment should make this taxonomy configurable and should evaluate it against labelled resumes.

### 4.3 Scoring

The score is deliberately transparent:

| Component | Weight | Interpretation |
|---|---:|---|
| Skill coverage | 55% | Percentage of detected job skills also present in the resume. |
| TF-IDF similarity | 30% | Similarity between resume and job-description vocabulary. |
| Experience evidence | 15% | Alignment between explicit years of experience in both texts. |

The three components are displayed independently. This avoids presenting one opaque percentage and gives the candidate a direct path to improvement.

## 5. Evaluation plan

A serious evaluation should use a labelled set of resume–job pairs with relevance ratings from human reviewers. Recommended metrics include mean absolute error between the application score and reviewer rating, ranking correlation, precision at a chosen shortlist size, and skill-extraction precision/recall. The current repository includes unit tests for core behavior but does not claim production-level benchmark performance because no labelled dataset is bundled.

## 6. Testing

The test suite covers alias canonicalisation, high-alignment matching, missing-skill detection, text normalisation and section parsing. Run it from the project root:

```bash
pytest -q
```

Additional tests should be added for malformed files, scanned PDFs, duplicate aliases, multilingual resumes, empty sections and adversarial text containing skill names only in irrelevant contexts.

## 7. Limitations

The baseline is not a semantic language model and may miss synonyms outside the configured taxonomy. TF-IDF can reward vocabulary overlap even when the underlying experience is weak. PDF extraction quality depends on whether the document contains selectable text; scanned documents require OCR. The experience heuristic relies on explicit year expressions and cannot validate employment history. Finally, the score is not a hiring recommendation and must not be used to make employment decisions without qualified human review.

## 8. Future roadmap

The next version can introduce sentence-transformer embeddings as a separately measured semantic baseline, a configurable taxonomy, robust entity and section extraction, OCR for scanned documents, a labelled evaluation workflow, and a RAG-based resume coach. An agentic extension could analyse missing skills, propose a learning plan, generate interview questions and verify recommendations against the job description. Each extension should preserve the current explainability and evaluation discipline.

## 9. Conclusion

ResumeIQ demonstrates how a small but complete AI product can combine data processing, classical machine learning, explainability and a deployable UI. Its strongest portfolio value comes not from claiming an inflated accuracy number, but from showing a clear problem definition, modular implementation, transparent scoring, responsible-use boundaries and a roadmap toward GenAI and agentic workflows.
