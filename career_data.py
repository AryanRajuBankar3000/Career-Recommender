"""
career_data.py
Small curated database of career paths used by the recommender.

Each career has:
- category      : broad domain, used for grouping
- description   : plain-English text used for TF-IDF interest matching
- core_skills   : skills that really define the role (weighted heavily)
- nice_to_have  : skills that help but aren't dealbreakers (weighted lightly)
"""

CAREERS = {
    "Data Scientist": {
        "category": "Data & AI",
        "description": (
            "Analyzes complex datasets using statistics and machine learning to find patterns, "
            "build predictive models, and turn data into business decisions."
        ),
        "core_skills": ["python", "machine learning", "statistics", "sql", "data analysis", "pandas"],
        "nice_to_have": ["deep learning", "r", "tableau", "aws", "data visualization", "numpy"],
    },
    "Machine Learning Engineer": {
        "category": "Data & AI",
        "description": (
            "Designs, builds, and deploys machine learning models and pipelines into production "
            "systems, focusing on scalability and engineering rigor."
        ),
        "core_skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch"],
        "nice_to_have": ["docker", "kubernetes", "aws", "sql", "computer vision", "nlp"],
    },
    "AI Research Scientist": {
        "category": "Data & AI",
        "description": (
            "Conducts original research to advance machine learning and artificial intelligence, "
            "publishing papers and prototyping novel model architectures."
        ),
        "core_skills": ["python", "deep learning", "machine learning", "statistics", "pytorch"],
        "nice_to_have": ["nlp", "computer vision", "tensorflow", "r"],
    },
    "Data Analyst": {
        "category": "Data & AI",
        "description": (
            "Explores and visualizes data to answer business questions, builds dashboards and "
            "reports, and communicates insights to stakeholders."
        ),
        "core_skills": ["sql", "excel", "data analysis", "data visualization", "tableau"],
        "nice_to_have": ["python", "power bi", "statistics", "communication"],
    },
    "Data Engineer": {
        "category": "Data & AI",
        "description": (
            "Builds and maintains the pipelines and infrastructure that move and transform data "
            "reliably at scale for analytics and machine learning teams."
        ),
        "core_skills": ["python", "sql", "spark", "big data", "aws"],
        "nice_to_have": ["hadoop", "docker", "kubernetes", "nosql", "postgresql"],
    },
    "Backend Developer": {
        "category": "Software Engineering",
        "description": (
            "Builds server-side logic, APIs, and databases that power applications, focusing on "
            "performance, reliability, and system design."
        ),
        "core_skills": ["python", "java", "sql", "rest api", "django"],
        "nice_to_have": ["node.js", "flask", "docker", "postgresql", "mongodb", "c#"],
    },
    "Frontend Developer": {
        "category": "Software Engineering",
        "description": (
            "Builds user-facing interfaces for websites and web apps, translating design into "
            "responsive, interactive code."
        ),
        "core_skills": ["javascript", "html", "css", "react"],
        "nice_to_have": ["typescript", "vue", "angular", "figma"],
    },
    "Full Stack Developer": {
        "category": "Software Engineering",
        "description": (
            "Works across both frontend and backend, building complete web applications end to "
            "end, from database to user interface."
        ),
        "core_skills": ["javascript", "python", "react", "sql", "rest api"],
        "nice_to_have": ["node.js", "html", "css", "django", "mongodb"],
    },
    "Mobile App Developer": {
        "category": "Software Engineering",
        "description": (
            "Builds native or cross-platform mobile applications for iOS and Android devices."
        ),
        "core_skills": ["swift", "kotlin", "java", "android", "ios"],
        "nice_to_have": ["react native", "flutter", "rest api"],
    },
    "DevOps Engineer": {
        "category": "Infrastructure & Cloud",
        "description": (
            "Automates deployment pipelines and manages infrastructure to help teams ship "
            "software faster and more reliably."
        ),
        "core_skills": ["linux", "docker", "kubernetes", "ci/cd", "aws"],
        "nice_to_have": ["terraform", "jenkins", "python", "azure"],
    },
    "Cloud Engineer": {
        "category": "Infrastructure & Cloud",
        "description": (
            "Designs, deploys, and manages scalable cloud infrastructure and services on "
            "platforms like AWS, Azure, or GCP."
        ),
        "core_skills": ["aws", "azure", "gcp", "linux", "docker"],
        "nice_to_have": ["terraform", "kubernetes", "python", "networking"],
    },
    "Cybersecurity Analyst": {
        "category": "Infrastructure & Cloud",
        "description": (
            "Monitors, detects, and responds to security threats, and hardens systems against "
            "attacks and vulnerabilities."
        ),
        "core_skills": ["network security", "penetration testing", "linux", "firewall"],
        "nice_to_have": ["siem", "encryption", "python", "cloud security"],
    },
    "QA / Test Engineer": {
        "category": "Software Engineering",
        "description": (
            "Designs and runs manual and automated tests to catch bugs and ensure software "
            "quality before release."
        ),
        "core_skills": ["test automation", "selenium", "manual testing", "qa"],
        "nice_to_have": ["python", "java", "junit", "ci/cd"],
    },
    "UX/UI Designer": {
        "category": "Design & Product",
        "description": (
            "Researches user needs and designs intuitive, visually polished interfaces and "
            "user flows for digital products."
        ),
        "core_skills": ["figma", "ui/ux", "wireframing", "prototyping"],
        "nice_to_have": ["sketch", "adobe xd", "photoshop", "user research"],
    },
    "Product Manager": {
        "category": "Design & Product",
        "description": (
            "Defines product strategy and roadmap, works across engineering, design, and "
            "business to ship features that solve user problems."
        ),
        "core_skills": ["product management", "communication", "agile", "market research"],
        "nice_to_have": ["sql", "data analysis", "scrum", "leadership"],
    },
    "Business Analyst": {
        "category": "Design & Product",
        "description": (
            "Bridges business needs and technical solutions by gathering requirements, "
            "analyzing processes, and recommending improvements."
        ),
        "core_skills": ["data analysis", "excel", "communication", "sql"],
        "nice_to_have": ["tableau", "power bi", "agile", "market research"],
    },
    "Digital Marketing Specialist": {
        "category": "Marketing & Sales",
        "description": (
            "Plans and runs online marketing campaigns across search, social, and content "
            "channels to grow audience and revenue."
        ),
        "core_skills": ["seo", "sem", "content marketing", "google analytics"],
        "nice_to_have": ["social media", "email marketing", "crm", "communication"],
    },
    "Sales Engineer": {
        "category": "Marketing & Sales",
        "description": (
            "Combines technical knowledge with sales skills to demo products, answer technical "
            "questions, and support the sales process for complex products."
        ),
        "core_skills": ["communication", "crm", "salesforce", "product management"],
        "nice_to_have": ["sql", "python", "presentation"],
    },
    "Project Manager": {
        "category": "Design & Product",
        "description": (
            "Plans, organizes, and oversees projects and teams to deliver work on time, on "
            "budget, and to scope."
        ),
        "core_skills": ["project management", "agile", "scrum", "communication", "leadership"],
        "nice_to_have": ["jira", "excel", "risk management"],
    },
    "Technical Writer": {
        "category": "Design & Product",
        "description": (
            "Writes clear documentation, guides, and manuals that explain technical products "
            "and processes to different audiences."
        ),
        "core_skills": ["technical writing", "documentation", "communication"],
        "nice_to_have": ["markdown", "api documentation", "editing"],
    },
}
