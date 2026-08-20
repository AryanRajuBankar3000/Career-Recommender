 AI Career Reality Check

A small ML/NLP project that reads someone's resume, compares it against
what they *say* they want to do, and gives an honest, skill-based
"reality check" plus a priority-ranked list of career recommendations.

Built to be understandable end-to-end in about an hour — no black-box
model, every score traces back to a specific matched or missing skill.

## How it works

1. **Resume input** — upload a `.pdf` / `.docx` / `.txt` file, or paste
   resume text directly.
2. **Skill extraction** — `skill_extractor.py` scans the resume text
   against a curated taxonomy of ~100 skills (with common aliases like
   "ML" → "machine learning") using regex keyword matching.
3. **Interest matching** — `recommender.py` uses **TF-IDF + cosine
   similarity** (scikit-learn) to compare the user's free-text
   description of what they want to do against a short description of
   each of the 20 careers in `career_data.py`.
4. **Qualification scoring** — for each career, computes what % of its
   *core* and *nice-to-have* skills the user's resume actually covers
   (core skills weighted 75%, nice-to-have 25%).
5. **Reality check** — for the user's stated dream career, compares
   interest vs. qualification, surfaces the gap, and lists exactly
   which core skills are missing.
6. **Prioritized recommendations** — blends qualification (60%) and
   interest (40%) into one ranked list, labeling each career as:
   - 🟢 **Best Fit** — high interest and already qualified
   - 🟡 **Stretch Goal** — high interest, real skill gaps to close
   - 🔵 **Hidden Strength** — qualified, even though not stated as a goal
   - ⚪ **Worth Exploring** — moderate on both fronts

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

Try it quickly with the included `sample_resume.txt` — paste its
contents into the "Paste text" option, and try an interest statement
like: *"I want to become a machine learning engineer and build AI
models."*

## Project structure

```
career-recommender/
├── app.py               # Streamlit UI — glue code only
├── career_data.py        # 20 careers: description + core/nice-to-have skills
├── skill_extractor.py    # Resume file reading + keyword-based skill extraction
├── recommender.py        # TF-IDF interest scoring + qualification scoring + ranking
├── sample_resume.txt      # Sample resume to try the app with
└── requirements.txt
```

## Extending it (ideas if you have more time)

- Swap keyword matching for a proper NER model (e.g. spaCy) to catch
  skills phrased in unusual ways.
- Replace TF-IDF interest matching with sentence embeddings
  (e.g. `sentence-transformers`) for better semantic matching.
- Add an "experience depth" signal (not just skill presence) using
  years-per-skill extraction.
- Let users edit/confirm the extracted skill list before scoring.
- Persist results so a user can track skill-gap progress over time.
