"""Streamlit entry point for the Resume–Job Matcher."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.matcher import match_resume_to_job  # noqa: E402
from src.parser import clean_text, estimate_contact_fields, extract_text, split_sections  # noqa: E402

st.set_page_config(page_title="ResumeIQ | Job Match Analyzer", page_icon="R", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .block-container {max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem;}
    .hero {padding: 1.5rem 1.7rem; border-radius: 18px; background: linear-gradient(135deg,#171B26 0%,#252044 100%); border: 1px solid #343954; margin-bottom: 1.5rem;}
    .hero h1 {font-size: 2.5rem; margin: 0; letter-spacing: -0.04em;}
    .hero p {color:#B9C0D4; font-size:1.05rem; margin-top:.6rem; margin-bottom:0;}
    .metric-card {background:#171B26; border:1px solid #2A3044; border-radius:14px; padding:1rem; min-height:115px;}
    .metric-label {color:#9EA6BC; font-size:.85rem; text-transform:uppercase; letter-spacing:.08em;}
    .metric-value {font-size:2rem; font-weight:700; margin-top:.35rem;}
    .tag {display:inline-block; padding:.35rem .65rem; border-radius:999px; background:#252044; color:#D8D3FF; margin:.25rem .25rem .25rem 0; font-size:.85rem; border:1px solid #484078;}
    .tag-missing {background:#3A202A; color:#FFB8C4; border-color:#75404B;}
    .small-muted {color:#9EA6BC; font-size:.9rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

SAMPLE_RESUME = """Aarav Sharma\nPython Developer | Machine Learning Enthusiast\naarav@example.com | github.com/aarav\n\nSUMMARY\nPython developer with 1.5 years of experience building data analysis and machine learning solutions.\n\nSKILLS\nPython, pandas, NumPy, scikit-learn, SQL, Git, Streamlit, data visualization, machine learning\n\nPROJECTS\nCustomer churn prediction using feature engineering, Random Forest and model deployment with Streamlit.\nBuilt a sales dashboard with Python and data visualization.\n\nEDUCATION\nB.Tech in Computer Science\n"""

SAMPLE_JOB = """Machine Learning Intern\n\nWe are looking for a candidate with Python, SQL, pandas, NumPy, scikit-learn and machine learning fundamentals. The candidate should understand feature engineering, data visualization, model evaluation and Git. Experience with Streamlit, deep learning or NLP is a plus. Candidates should communicate insights clearly and work with stakeholders.\n\nResponsibilities: clean datasets, train baseline models, evaluate experiments, build dashboards and document results."""


def render_tags(items: list[str], missing: bool = False) -> None:
    if not items:
        st.caption("No skills detected from the available taxonomy.")
        return
    css = "tag tag-missing" if missing else "tag"
    html = "".join(f'<span class="{css}">{item}</span>' for item in items)
    st.markdown(html, unsafe_allow_html=True)


def score_chart(result) -> None:
    labels = ["Overall match", "Skill coverage", "Text similarity", "Evidence"]
    values = [result.overall_score, result.skill_score, result.semantic_score, result.evidence_score]
    fig = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color=["#7C6FF2", "#50C878", "#58A6FF", "#F2B84B"], text=[f"{v:.1f}%" for v in values], textposition="auto"))
    fig.update_layout(height=250, margin=dict(l=0, r=20, t=10, b=10), xaxis=dict(range=[0, 100], title="Score (%)"), yaxis=dict(autorange="reversed"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#F4F6FB"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def main() -> None:
    st.markdown('<div class="hero"><h1>ResumeIQ</h1><p>Explainable resume-to-job matching for faster, evidence-based applications.</p></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("How it works")
        st.write("Upload a resume, add a job description, and receive a transparent match score based on skill coverage, text similarity and experience evidence.")
        st.divider()
        st.caption("Privacy-first demo")
        st.caption("Uploaded documents are processed in memory by this local application and are not persisted by the app.")
        if st.button("Load sample data", use_container_width=True):
            st.session_state["resume_text"] = SAMPLE_RESUME
            st.session_state["job_text"] = SAMPLE_JOB
            st.rerun()

    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("1. Add your resume")
        uploaded = st.file_uploader("PDF, DOCX, TXT or MD", type=["pdf", "docx", "txt", "md"], label_visibility="collapsed")
        if uploaded is not None:
            try:
                st.session_state["resume_text"] = clean_text(extract_text(uploaded.getvalue(), uploaded.name))
                st.success(f"Parsed {uploaded.name}")
            except ValueError as exc:
                st.error(str(exc))
        resume_text = st.text_area("Resume text", value=st.session_state.get("resume_text", ""), height=310, placeholder="Paste your resume text or upload a document...")
        st.session_state["resume_text"] = resume_text

    with right:
        st.subheader("2. Add the job description")
        job_upload = st.file_uploader("Optional job description file", type=["pdf", "docx", "txt", "md"], key="job_file", label_visibility="collapsed")
        if job_upload is not None:
            try:
                st.session_state["job_text"] = clean_text(extract_text(job_upload.getvalue(), job_upload.name))
                st.success(f"Parsed {job_upload.name}")
            except ValueError as exc:
                st.error(str(exc))
        job_text = st.text_area("Job description", value=st.session_state.get("job_text", ""), height=310, placeholder="Paste the complete job description here...")
        st.session_state["job_text"] = job_text

    analyze = st.button("Analyze match", type="primary", use_container_width=True)
    if analyze:
        if len(resume_text.strip()) < 40 or len(job_text.strip()) < 40:
            st.warning("Please provide at least 40 characters for both the resume and job description.")
            return
        st.session_state["result"] = match_resume_to_job(resume_text, job_text)

    result = st.session_state.get("result")
    if result is None:
        st.info("Add both documents and select **Analyze match**. Use sample data from the sidebar to preview the workflow.")
        return

    st.divider()
    st.subheader("Match report")
    c1, c2, c3, c4 = st.columns(4)
    cards = [(c1, "Overall match", f"{result.overall_score:.1f}%"), (c2, "Skill coverage", f"{result.skill_score:.1f}%"), (c3, "Text similarity", f"{result.semantic_score:.1f}%"), (c4, "Evidence signal", f"{result.evidence_score:.1f}%")]
    for column, label, value in cards:
        with column:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

    col_chart, col_detail = st.columns([1.1, 1], gap="large")
    with col_chart:
        st.markdown("#### Score breakdown")
        score_chart(result)
    with col_detail:
        st.markdown("#### What to do next")
        for recommendation in result.recommendations:
            st.write("→", recommendation)
        contact = estimate_contact_fields(resume_text)
        st.markdown("#### Resume completeness signals")
        labels = {"email": "Email", "phone": "Phone", "linkedin": "LinkedIn", "github": "GitHub"}
        st.write(" · ".join(("✓ " if value else "○ ") + labels[key] for key, value in contact.items()))

    skill_left, skill_right = st.columns(2, gap="large")
    with skill_left:
        st.markdown("#### Matched skills")
        render_tags(result.matched_skills)
    with skill_right:
        st.markdown("#### Skills to strengthen")
        render_tags(result.missing_skills, missing=True)

    with st.expander("View detected sections and transparent methodology"):
        sections = split_sections(resume_text)
        section_df = pd.DataFrame({"Section": list(sections.keys()), "Characters": [len(value) for value in sections.values()]})
        st.dataframe(section_df, hide_index=True, use_container_width=True)
        st.markdown("The score is a weighted blend of skill coverage (55%), TF-IDF text similarity (30%) and experience evidence (15%). It is an assistive signal, not a hiring decision.")


if __name__ == "__main__":
    main()
