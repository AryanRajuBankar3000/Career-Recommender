"""
app.py
Streamlit front-end for the AI Career Reality Check project.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd

from skill_extractor import extract_text_from_file, extract_skills, extract_years_of_experience
from recommender import (
    CAREER_NAMES,
    compute_interest_scores,
    compute_qualification_scores,
    reality_check,
    prioritized_recommendations,
)

st.set_page_config(page_title="Career Reality Check", page_icon="🎯", layout="centered")

st.title("🎯 AI Career Reality Check")
st.write(
    "Upload your resume, tell us what career you *want*, and get an honest, "
    "skill-based read on how ready you are — plus a priority-ranked list of "
    "careers that actually fit your current skill set."
)

# ---------------------------------------------------------------- STEP 1: RESUME
st.header("1. Your resume")
resume_mode = st.radio("How do you want to provide your resume?", ["Upload a file", "Paste text"], horizontal=True)

resume_text = ""
if resume_mode == "Upload a file":
    uploaded = st.file_uploader("Upload resume (.pdf, .docx, or .txt)", type=["pdf", "docx", "txt"])
    if uploaded is not None:
        try:
            resume_text = extract_text_from_file(uploaded)
            st.success(f"Read {len(resume_text.split())} words from {uploaded.name}")
        except Exception as e:
            st.error(f"Couldn't read that file: {e}")
else:
    resume_text = st.text_area("Paste your resume text here", height=220, placeholder="Paste your resume content...")

# ---------------------------------------------------------------- STEP 2: INTEREST
st.header("2. What career do you actually want?")
dream_career = st.selectbox(
    "Pick the career closest to your goal (used for the reality check):",
    options=CAREER_NAMES,
)
interest_text = st.text_area(
    "In your own words, describe your interests and the kind of work you want to do",
    height=140,
    placeholder="e.g. I love working with data, I want to build AI models and work on machine learning projects...",
)

# ---------------------------------------------------------------- STEP 3: ANALYZE
st.header("3. Get your reality check")
analyze_clicked = st.button("Analyze me", type="primary", use_container_width=True)

if analyze_clicked:
    if not resume_text.strip():
        st.warning("Please upload or paste your resume first.")
    elif not interest_text.strip():
        st.warning("Please describe your career interests first.")
    else:
        with st.spinner("Extracting skills and scoring careers..."):
            user_skills = extract_skills(resume_text)
            years = extract_years_of_experience(resume_text)
            interest_scores = compute_interest_scores(interest_text)
            qualification = compute_qualification_scores(user_skills)
            rc = reality_check(dream_career, interest_scores, qualification)
            recs = prioritized_recommendations(interest_scores, qualification)

        # ---- Extracted skills
        st.subheader("Skills we found in your resume")
        if user_skills:
            st.write(" ".join(f"`{s}`" for s in sorted(user_skills)))
        else:
            st.info("No recognized skills found — try pasting more of your resume, or listing skills explicitly.")
        if years:
            st.caption(f"Estimated experience: ~{years} years (heuristic, based on text like '{years} years')")

        st.divider()

        # ---- Reality check
        st.subheader(f"Reality check: {dream_career}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Your interest", f"{rc['interest_score']}%")
        col2.metric("Your qualification", f"{rc['qualification_score']}%")
        col3.metric("Gap", f"{rc['gap']}%", delta=None)

        st.write(f"**Verdict:** {rc['verdict']}")

        if rc["matched_core_skills"]:
            st.write("✅ **Core skills you already have:** " + ", ".join(rc["matched_core_skills"]))
        if rc["missing_core_skills"]:
            st.write("⚠️ **Core skills you're missing:** " + ", ".join(rc["missing_core_skills"]))
        else:
            st.write("You already cover every core skill for this role — the gap, if any, is about depth/experience, not missing basics.")

        st.divider()

        # ---- Prioritized recommendations
        st.subheader("Your priority-ranked career recommendations")
        st.caption(
            "Ranked by a blend of 60% how qualified you are + 40% how well it matches your stated interest — "
            "so this won't just flatter you, and won't ignore what you're good at either."
        )

        df = pd.DataFrame(recs)
        df_display = df[["career", "category", "label", "qualification_score", "interest_score", "blended_score"]]
        df_display.columns = ["Career", "Category", "Label", "Qualification %", "Interest %", "Priority Score"]
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.bar_chart(df.set_index("career")[["qualification_score", "interest_score"]])

        label_legend = {
            "Best Fit": "🟢 High interest AND you're already qualified.",
            "Stretch Goal": "🟡 High interest, but real skill gaps — needs upskilling.",
            "Hidden Strength": "🔵 You're qualified even though you didn't say you're interested — worth a look.",
            "Worth Exploring": "⚪ Moderate on both fronts — worth investigating further.",
        }
        with st.expander("What do the labels mean?"):
            for label, meaning in label_legend.items():
                st.write(f"**{label}** — {meaning}")

        for r in recs:
            if r["label"] == "Stretch Goal" and r["missing_core_skills"]:
                st.write(
                    f"📌 To make **{r['career']}** realistic, focus on: "
                    + ", ".join(r["missing_core_skills"])
                )
