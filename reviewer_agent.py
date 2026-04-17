# reviewer_agent.py — AI Portfolio Reviewer Core Logic

import os
import json
import requests
import tempfile
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ── Fetch GitHub profile ──────────────────────────────────────
def fetch_github_profile(username: str) -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        user_resp = requests.get(
            f"https://api.github.com/users/{username}",
            headers=headers, timeout=10
        )
        if user_resp.status_code == 404:
            return {"error": f"GitHub user '{username}' not found"}

        user_data = user_resp.json()

        repos_resp = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=20&sort=updated",
            headers=headers, timeout=10
        )
        repos_data = repos_resp.json()

        repos = []
        languages = set()
        for repo in repos_data:
            if not repo.get("fork"):
                repos.append({
                    "name":        repo["name"],
                    "description": repo.get("description", "No description"),
                    "language":    repo.get("language", "Unknown"),
                    "stars":       repo.get("stargazers_count", 0),
                    "updated":     repo.get("updated_at", "")[:10]
                })
                if repo.get("language"):
                    languages.add(repo["language"])

        return {
            "username":     username,
            "name":         user_data.get("name", username),
            "bio":          user_data.get("bio", "No bio"),
            "followers":    user_data.get("followers", 0),
            "public_repos": user_data.get("public_repos", 0),
            "languages":    list(languages),
            "repos":        repos[:10]
        }
    except Exception as e:
        return {"error": str(e)}

# ── Extract resume text from PDF ──────────────────────────────
def extract_resume_text(pdf_file) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file.read())
            tmp_path = tmp.name

        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
        os.unlink(tmp_path)
        return "\n".join(page.page_content for page in pages)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# ── Analyse resume ────────────────────────────────────────────
def analyse_resume(resume_text: str) -> dict:
    prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter and career coach.

Analyse this resume and return ONLY a JSON object.
No markdown, no explanation, no backticks — pure JSON only.

RESUME:
{resume}

Return this exact JSON structure:
{{
    "current_role": "current or most recent job title",
    "years_experience": "estimated total years",
    "technical_skills": ["skill1", "skill2"],
    "ai_ml_skills": ["any AI/ML skills found"],
    "strengths": ["top 3 strengths"],
    "weaknesses": ["top 3 gaps for AI engineering"],
    "education": "highest education level",
    "overall_score": 0
}}

Score out of 100 for AI engineering readiness.
Return ONLY valid JSON — absolutely no other text.
""")

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"resume": resume_text[:3000]})

    try:
        result = result.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except:
        return {
            "current_role":     "Unable to parse",
            "years_experience": "Unknown",
            "technical_skills": [],
            "ai_ml_skills":     [],
            "strengths":        [],
            "weaknesses":       [],
            "education":        "Unknown",
            "overall_score":    0
        }

# ── Analyse GitHub ────────────────────────────────────────────
def analyse_github(github_data: dict) -> dict:
    if "error" in github_data:
        return {"error": github_data["error"]}

    prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter reviewing a GitHub profile.

GitHub Profile:
{github}

Return ONLY a JSON object — no markdown, no explanation, no backticks:
{{
    "github_score": 0,
    "ai_projects": ["list any AI/ML related repos"],
    "main_languages": ["top languages used"],
    "profile_strengths": ["what looks good"],
    "profile_gaps": ["what is missing for AI engineering"],
    "repo_count": 0,
    "activity_level": "active/moderate/inactive"
}}

Score out of 100 for AI engineering portfolio quality.
Return ONLY valid JSON — absolutely no other text.
""")

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"github": json.dumps(github_data, indent=2)})

    try:
        result = result.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except:
        return {
            "github_score":      0,
            "ai_projects":       [],
            "main_languages":    github_data.get("languages", []),
            "profile_strengths": [],
            "profile_gaps":      [],
            "repo_count":        github_data.get("public_repos", 0),
            "activity_level":    "unknown"
        }

# ── Generate action plan ──────────────────────────────────────
def generate_action_plan(
    resume_analysis:  dict,
    github_analysis:  dict,
    target_role:      str,
    current_learning: str = ""
) -> dict:

    prompt = ChatPromptTemplate.from_template("""
You are an expert AI career coach giving personalised advice.

TARGET ROLE: {target_role}

RESUME ANALYSIS:
{resume}

GITHUB ANALYSIS:
{github}

WHAT THEY ARE CURRENTLY LEARNING/BUILDING:
{current_learning}

IMPORTANT RULES:
- Factor in what they are currently building
- Do NOT recommend things they are already doing
- Give advice that goes BEYOND their current learning
- Be specific to their SRE/infrastructure background
- Recommend advanced next steps not beginner ones

Return ONLY a JSON object — no markdown, no explanation, no backticks:
{{
    "overall_score": 0,
    "hire_readiness": "Not Ready / Getting There / Almost Ready / Ready",
    "summary": "2-3 sentence honest assessment based on their actual background",
    "immediate_actions": [
        {{"action": "specific action", "why": "why it matters", "time": "how long"}}
    ],
    "projects_to_build": [
        {{"project": "project name", "skills_gained": "specific skills", "priority": "high/medium/low"}}
    ],
    "skills_to_learn": [
        {{"skill": "specific skill", "resource": "exact resource name", "time": "estimated time"}}
    ],
    "resume_fixes": ["specific fix 1", "specific fix 2", "specific fix 3"],
    "github_fixes": ["specific fix 1", "specific fix 2", "specific fix 3"],
    "timeline": "realistic timeline to be job ready"
}}

Be honest, specific and avoid generic advice.
Return ONLY valid JSON — absolutely no other text.
""")

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({
        "target_role":      target_role,
        "resume":           json.dumps(resume_analysis, indent=2),
        "github":           json.dumps(github_analysis, indent=2),
        "current_learning": current_learning or "Not specified"
    })

    try:
        result = result.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    except:
        return {
            "overall_score":     0,
            "hire_readiness":    "Unable to parse",
            "summary":           result,
            "immediate_actions": [],
            "projects_to_build": [],
            "skills_to_learn":   [],
            "resume_fixes":      [],
            "github_fixes":      [],
            "timeline":          "Unknown"
        }