"""
skill_extractor.py
Reads resumes (pdf / docx / txt / pasted text) and extracts a normalized
set of skills using a keyword + alias matching approach.

This is intentionally kept as transparent keyword matching (not a black-box
model) so the "reality check" scores stay explainable — you can always
answer "why did it say I don't have X skill".
"""

import re
import io

# canonical_skill -> list of alternate spellings / abbreviations to catch in resume text
SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java(?!script)"],
    "javascript": ["javascript", r"\bjs\b"],
    "typescript": ["typescript", r"\bts\b"],
    "c++": [r"c\+\+"],
    "c#": [r"c#"],
    "r": [r"\br\b(?=.{0,20}(programming|studio|language|stats|statistics))", r"\br programming\b"],
    "go": [r"\bgolang\b"],
    "ruby": ["ruby"],
    "php": ["php"],
    "swift": ["swift"],
    "kotlin": ["kotlin"],
    "html": ["html5?"],
    "css": ["css3?"],
    "sql": [r"\bsql\b", "mysql", "postgresql", "t-sql", "pl/sql"],
    "nosql": ["nosql"],
    "mongodb": ["mongodb", "mongo db"],
    "postgresql": ["postgresql", "postgres"],
    "machine learning": ["machine learning", r"\bml\b"],
    "deep learning": ["deep learning", r"\bdl\b"],
    "nlp": ["natural language processing", r"\bnlp\b"],
    "computer vision": ["computer vision", r"\bcv\b(?=.{0,20}(image|vision))"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch", "torch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data viz"],
    "statistics": ["statistics", "statistical analysis"],
    "tableau": ["tableau"],
    "power bi": ["power bi", "powerbi"],
    "excel": ["excel", "ms excel"],
    "big data": ["big data"],
    "spark": ["apache spark", r"\bspark\b"],
    "hadoop": ["hadoop"],
    "react": [r"\breact\b", "react\\.?js", "reactjs"],
    "angular": ["angular"],
    "vue": [r"\bvue\b", "vue\\.?js"],
    "node.js": ["node\\.?js"],
    "django": ["django"],
    "flask": ["flask"],
    "rest api": ["rest api", "restful", "rest apis"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", r"\bk8s\b"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous deployment"],
    "terraform": ["terraform"],
    "jenkins": ["jenkins"],
    "linux": ["linux", "unix"],
    "networking": ["networking", "computer networks"],
    "network security": ["network security"],
    "penetration testing": ["penetration testing", "pen testing"],
    "firewall": ["firewall"],
    "siem": ["siem"],
    "encryption": ["encryption", "cryptography"],
    "cloud security": ["cloud security"],
    "test automation": ["test automation", "automated testing"],
    "selenium": ["selenium"],
    "manual testing": ["manual testing"],
    "qa": [r"\bqa\b", "quality assurance"],
    "junit": ["junit"],
    "figma": ["figma"],
    "ui/ux": ["ui/ux", r"\bux\b", r"\bui\b"],
    "wireframing": ["wireframing", "wireframe"],
    "prototyping": ["prototyping", "prototype"],
    "sketch": ["sketch(?=.{0,15}(design|app))"],
    "adobe xd": ["adobe xd"],
    "photoshop": ["photoshop"],
    "user research": ["user research"],
    "product management": ["product management", "product manager"],
    "communication": ["communication skills", "communication"],
    "agile": ["agile"],
    "scrum": ["scrum"],
    "market research": ["market research"],
    "leadership": ["leadership"],
    "seo": [r"\bseo\b"],
    "sem": [r"\bsem\b"],
    "content marketing": ["content marketing"],
    "google analytics": ["google analytics"],
    "social media": ["social media marketing", "social media"],
    "email marketing": ["email marketing"],
    "crm": [r"\bcrm\b"],
    "salesforce": ["salesforce"],
    "presentation": ["presentation skills"],
    "project management": ["project management"],
    "jira": ["jira"],
    "risk management": ["risk management"],
    "technical writing": ["technical writing"],
    "documentation": ["documentation"],
    "markdown": ["markdown"],
    "api documentation": ["api documentation"],
    "editing": ["copy editing", "editing"],
    "android": ["android"],
    "ios": ["ios"],
    "react native": ["react native"],
    "flutter": ["flutter"],
}

# Pre-compile regex patterns once
_COMPILED_ALIASES = {
    skill: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for skill, patterns in SKILL_ALIASES.items()
}


def extract_text_from_file(uploaded_file) -> str:
    """
    Extracts raw text from an uploaded resume file.
    Accepts a file-like object with a `.name` attribute (as Streamlit's
    UploadedFile provides) for .pdf, .docx, or .txt files.
    """
    name = uploaded_file.name.lower()
    raw_bytes = uploaded_file.read()

    if name.endswith(".pdf"):
        return _extract_pdf_text(raw_bytes)
    elif name.endswith(".docx"):
        return _extract_docx_text(raw_bytes)
    elif name.endswith(".txt"):
        return raw_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {name}. Please upload .pdf, .docx, or .txt")


def _extract_pdf_text(raw_bytes: bytes) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(io.BytesIO(raw_bytes))
    text_parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_parts)


def _extract_docx_text(raw_bytes: bytes) -> str:
    import docx
    document = docx.Document(io.BytesIO(raw_bytes))
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def extract_skills(text: str) -> set:
    """
    Scans resume text and returns the set of canonical skills found,
    based on keyword/alias matching.
    """
    found = set()
    for skill, patterns in _COMPILED_ALIASES.items():
        for pattern in patterns:
            if pattern.search(text):
                found.add(skill)
                break
    return found


def extract_years_of_experience(text: str):
    """
    Best-effort heuristic: looks for patterns like '5 years of experience'
    or '3+ years'. Returns the largest number found, or None.
    """
    matches = re.findall(r"(\d+)\+?\s*(?:years|yrs)\b", text, re.IGNORECASE)
    if not matches:
        return None
    return max(int(m) for m in matches)
