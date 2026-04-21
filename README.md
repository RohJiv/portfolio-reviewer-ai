# 🎯 AI Portfolio Reviewer & Career Mentor

An AI-powered career advisor that analyses your resume and GitHub profile, compares them to your target role, and generates a personalised action plan to make you hireable — with structured JSON output you can actually act on.

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![LangChain](https://img.shields.io/badge/framework-LangChain-yellow)

---

## 🎯 What It Does

Tired of generic career advice? This tool gives you specific, personalised recommendations:

- Upload your resume PDF
- Enter your GitHub username
- Select your target role (AI Engineer, ML Engineer, etc.)
- Describe what you're currently learning
- Get back a structured action plan in 5 tabs:
  - ⚡ Immediate actions (what to do right now)
  - 🏗️ Projects to build (specific ideas)
  - 📚 Skills to learn (with resources)
  - 📄 Resume fixes (exact improvements)
  - 🐙 GitHub fixes (profile improvements)

Plus: AI Engineering Readiness Score out of 100.

---

## 💡 Why I Built This

During my own career transition from SRE to AI engineering, I wished I had a tool that gave me honest, actionable feedback instead of vague advice like "learn deep learning."

So I built one. It analyses YOUR actual profile and tells you exactly what's missing — not generic advice that applies to everyone.

---

## 🏗️ Architecture

```
User Inputs
├── Resume PDF        → Extract text → Analyse skills
├── GitHub Username   → Fetch via API → Analyse projects
├── Target Role       → Context for analysis
└── Current Learning  → Avoid redundant suggestions
         ↓
Three parallel LLM analyses:
- Resume Analysis → JSON
- GitHub Analysis → JSON
- Action Plan Generation → JSON
         ↓
Structured Output → Streamlit Multi-tab UI
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📄 Resume PDF Analysis | Extracts skills, experience, and gaps |
| 🐙 Live GitHub Analysis | Fetches real-time repo data via GitHub API |
| 🎯 Target Role Matching | Compares profile to 5 common AI roles |
| 📚 Context-Aware Advice | Accounts for what you're already learning |
| 📊 Readiness Score | 0-100 scale with colour-coded indicators |
| 🏆 Hire-Readiness Level | Not Ready / Getting There / Almost / Ready |
| ⏱️ Timeline Estimate | Realistic time to job readiness |
| 🎨 Multi-Tab Dashboard | Organised, actionable feedback |

---

## 🛠️ Tech Stack

- **Framework:** LangChain
- **LLM:** OpenAI GPT-4 compatible APIs
- **GitHub Integration:** REST API via Requests
- **PDF Parsing:** PyPDF
- **UI:** Streamlit
- **Output Format:** Structured JSON

---

## 🚀 Run Locally

```bash
git clone https://github.com/RohJiv/portfolio-reviewer-ai.git
cd portfolio-reviewer-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

# Set .env
# OPENAI_API_KEY=your_key_here

streamlit run app.py
```

---

## 📖 Structured Output — Why It Matters

Most AI tools return free-text responses. This one returns **structured JSON**:

```json
{
  "overall_score": 72,
  "hire_readiness": "Almost Ready",
  "immediate_actions": [
    {"action": "Deploy projects to cloud", "why": "Live demos = credibility", "time": "1 day"}
  ],
  "projects_to_build": [...],
  "skills_to_learn": [...],
  "resume_fixes": [...],
  "github_fixes": [...]
}
```

**Why JSON output?**
- Enables beautiful UI rendering
- Can be saved, compared, tracked over time
- Analytics-ready for enterprise use
- Clean separation of data and presentation

This is production AI pattern — not tutorial chatbot behavior.

---

## 🎓 What I Learned Building This

- **Multi-source AI analysis** — resumes + GitHub + context
- **GitHub REST API integration** for live portfolio data
- **Structured LLM output** via JSON parsing
- **Multi-LLM orchestration** (3 chained analyses)
- **Error handling** for malformed JSON responses
- **Prompt engineering** for consistent structured output
- **Streamlit multi-tab UI design**

---

## 💼 Real-World Applications

This pattern is used in:
- Corporate learning platforms (personalised upskilling)
- Recruiter tools (automated candidate assessment)
- University career services (resume reviews at scale)
- Internal talent development programs
- L&D platforms (gap analysis for certifications)

---

## 🎯 Target Roles Supported

The tool provides tailored analysis for:
- AI Engineer
- ML Engineer
- LLM Application Developer
- AI Solutions Architect
- Data Scientist

---

## 🧪 Test It On Yourself

Perfect for:
- Students preparing for their first AI role
- Career switchers (my original use case)
- Existing developers adding AI skills
- Engineers targeting specific AI companies

---

## 🔐 Privacy Notes

- Resume data processed in-memory — never stored
- GitHub data fetched via public API only
- No personal data logged
- All analysis happens locally

---

## 👤 Author

**Phani Rajiv G**
Technical Program Manager | Cloud & AI Platforms
📍 Hyderabad, India
📧 phani.rg@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/phanirajivg)

Built this tool to help my own career transition. Sharing it so others can benefit too.

---

## 📄 License

MIT License — free to use for learning.

---

⭐ If this helped your career, star the repo!
