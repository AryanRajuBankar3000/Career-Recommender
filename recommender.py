"""
recommender.py
Turns (resume skills + free-text career interest) into:
  1. an "interest score" per career  -> how closely their stated interest matches each career (TF-IDF + cosine similarity)
  2. a "qualification score" per career -> how many of the required skills they actually have
  3. a reality check for their stated dream career
  4. a prioritized, labeled list of recommendations
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from career_data import CAREERS

CAREER_NAMES = list(CAREERS.keys())
CORE_WEIGHT = 0.75      # core skills count for 75% of the qualification score
NICE_WEIGHT = 0.25      # nice-to-have skills count for the remaining 25%


def compute_interest_scores(interest_text: str) -> dict:
    """
    Uses TF-IDF + cosine similarity between the user's free-text interest
    statement and each career's description to score how well their stated
    interest aligns with each career, on a 0-100 scale.
    """
    documents = [CAREERS[name]["description"] for name in CAREER_NAMES]
    documents.append(interest_text)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    user_vector = tfidf_matrix[-1]
    career_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(user_vector, career_vectors)[0]

    # Normalize so the top match is scaled sensibly for display (0-100)
    max_sim = similarities.max() if similarities.max() > 0 else 1
    scores = {
        name: round((sim / max_sim) * 100, 1)
        for name, sim in zip(CAREER_NAMES, similarities)
    }
    return scores


def compute_qualification_scores(user_skills: set) -> dict:
    """
    For each career, computes what % of its required skills the user
    actually has, weighting core skills more heavily than nice-to-haves.
    Also returns which core skills are missing, for the reality check.
    """
    results = {}
    for name, info in CAREERS.items():
        core = set(info["core_skills"])
        nice = set(info["nice_to_have"])

        core_have = user_skills & core
        nice_have = user_skills & nice

        core_pct = len(core_have) / len(core) if core else 0
        nice_pct = len(nice_have) / len(nice) if nice else 0

        score = round((core_pct * CORE_WEIGHT + nice_pct * NICE_WEIGHT) * 100, 1)

        results[name] = {
            "score": score,
            "matched_core": sorted(core_have),
            "missing_core": sorted(core - core_have),
            "matched_nice": sorted(nice_have),
        }
    return results


def reality_check(dream_career: str, interest_scores: dict, qualification: dict) -> dict:
    """
    Builds the "reality check" for the user's stated dream career:
    compares how much they want it vs. how qualified they currently are,
    and returns a verdict + concrete next steps.
    """
    interest = interest_scores.get(dream_career, 0)
    qual_info = qualification.get(dream_career, {"score": 0, "missing_core": [], "matched_core": []})
    qual_score = qual_info["score"]
    gap = interest - qual_score

    if qual_score >= 70:
        verdict = "You're genuinely well-qualified for this already."
    elif qual_score >= 40:
        verdict = "You're partway there — some real gaps to close, but it's realistic."
    elif gap > 30:
        verdict = "Big gap: your interest is high, but your current skills don't back it up yet."
    else:
        verdict = "Early stage — this would need meaningful upskilling before you're competitive."

    return {
        "career": dream_career,
        "interest_score": interest,
        "qualification_score": qual_score,
        "gap": round(gap, 1),
        "verdict": verdict,
        "matched_core_skills": qual_info["matched_core"],
        "missing_core_skills": qual_info["missing_core"],
    }


def prioritized_recommendations(interest_scores: dict, qualification: dict, top_n: int = 6) -> list:
    """
    Ranks all careers by a blended score (60% qualification, 40% interest —
    reality-weighted so we don't just recommend whatever they said they want)
    and labels each one so the ranking is easy to interpret at a glance.
    """
    ranked = []
    for name in CAREER_NAMES:
        interest = interest_scores.get(name, 0)
        qual = qualification[name]["score"]
        blended = round(qual * 0.6 + interest * 0.4, 1)

        if interest >= 40 and qual >= 55:
            label = "Best Fit"
        elif interest >= 40 and qual < 40:
            label = "Stretch Goal"
        elif interest < 30 and qual >= 55:
            label = "Hidden Strength"
        else:
            label = "Worth Exploring"

        ranked.append({
            "career": name,
            "category": CAREERS[name]["category"],
            "interest_score": interest,
            "qualification_score": qual,
            "blended_score": blended,
            "label": label,
            "missing_core_skills": qualification[name]["missing_core"],
        })

    ranked.sort(key=lambda x: x["blended_score"], reverse=True)
    return ranked[:top_n]
