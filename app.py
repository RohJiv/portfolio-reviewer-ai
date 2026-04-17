# app.py — AI Portfolio Reviewer & Career Mentor (Complete Final Version)

import streamlit as st
from reviewer_agent import (
    fetch_github_profile,
    extract_resume_text,
    analyse_resume,
    analyse_github,
    generate_action_plan
)
# Works locally (from .env) AND on Railway (from environment variables)
def get_api_key():
    # Try Streamlit secrets first (production)
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        # Fall back to .env (local development)
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("GROQ_API_KEY")
# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="🎯 Portfolio Reviewer",
    page_icon="🎯",
    layout="wide"
)

# ── Initialize session state ──────────────────────────────────
if "analysis_done" not in st.session_state:
    st.session_state["analysis_done"] = False

if "results" not in st.session_state:
    st.session_state["results"] = {}

# ── Title ─────────────────────────────────────────────────────
st.title("🎯 AI Portfolio Reviewer & Career Mentor")
st.caption("Upload your resume + GitHub → Get an exact action plan to get hired as an AI engineer")

# ── Input Form ────────────────────────────────────────────────
with st.form("review_form"):
    st.subheader("📋 Your Details")

    col1, col2 = st.columns([1, 1])

    with col1:
        resume_file = st.file_uploader(
            "📄 Upload your Resume (PDF)",
            type=["pdf"]
        )
        target_role = st.selectbox(
            "🎯 Target Role",
            [
                "AI Engineer",
                "ML Engineer",
                "LLM Application Developer",
                "AI Solutions Architect",
                "Data Scientist"
            ]
        )
        github_username = st.text_input(
            "🐙 GitHub Username",
            placeholder="e.g. sahaji123"
        )

    with col2:
        current_learning = st.text_area(
            "📚 What are you currently learning/building?",
            placeholder="""Example:
- Building RAG chatbots with LangChain and ChromaDB
- Built SQL Agent with natural language to SQL
- Learning LangGraph for AI workflows
- Using Groq API for fast LLM inference
- 10+ years SRE/Linux background""",
            height=200
        )
        st.info("""
**What this tool analyses:**
- ✅ Your current skills vs market demand
- ✅ GitHub portfolio quality
- ✅ Resume gaps and exact fixes
- ✅ Projects to build next
- ✅ Realistic timeline to get hired
        """)

    submit = st.form_submit_button(
        "🚀 Analyse My Portfolio",
        type="primary",
        use_container_width=True
    )

# ── Run Analysis ──────────────────────────────────────────────
if submit:
    if not resume_file and not github_username:
        st.error("❌ Please upload a resume OR enter a GitHub username")
    else:
        st.session_state["analysis_done"] = False
        results = {}

        # Analyse Resume
        if resume_file:
            with st.spinner("📄 Reading your resume..."):
                resume_text = extract_resume_text(resume_file)
            with st.spinner("🧠 Analysing resume..."):
                results["resume"] = analyse_resume(resume_text)
        else:
            results["resume"] = None

        # Analyse GitHub
        if github_username:
            with st.spinner(f"🐙 Fetching GitHub for {github_username}..."):
                github_data = fetch_github_profile(github_username)
            with st.spinner("🧠 Analysing GitHub portfolio..."):
                results["github"]     = analyse_github(github_data)
                results["github_raw"] = github_data
        else:
            results["github"]     = None
            results["github_raw"] = {}

        # Generate Action Plan
        with st.spinner("📋 Generating your personalised action plan..."):
            results["action_plan"] = generate_action_plan(
                results["resume"] or {},
                results["github"] or {},
                target_role,
                current_learning
            )

        st.session_state["results"]       = results
        st.session_state["analysis_done"] = True
        st.rerun()

# ── Display Results ───────────────────────────────────────────
if st.session_state["analysis_done"]:
    results   = st.session_state["results"]
    plan      = results["action_plan"]
    score     = plan.get("overall_score", 0)
    readiness = plan.get("hire_readiness", "Unknown")

    st.divider()

    # Score color
    color = "🟢" if score >= 75 else "🟡" if score >= 50 else "🔴"

    st.subheader(f"{color} AI Engineering Readiness: {score}/100")
    st.markdown(f"### {readiness}")
    st.info(plan.get("summary", ""))

    st.divider()

    # Top metrics
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric(
        "📄 Resume Score",
        f"{results['resume'].get('overall_score', 0)}/100"
        if results.get("resume") else "N/A"
    )
    sc2.metric(
        "🐙 GitHub Score",
        f"{results['github'].get('github_score', 0)}/100"
        if results.get("github") else "N/A"
    )
    sc3.metric(
        "⏱️ Timeline",
        plan.get("timeline", "Unknown")
    )

    st.divider()

    # ── Tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚡ Action Plan",
        "🏗️ Projects to Build",
        "📚 Skills to Learn",
        "📄 Resume Fixes",
        "🐙 GitHub Fixes"
    ])

    # Tab 1 — Immediate Actions
    with tab1:
        st.subheader("⚡ Do These RIGHT NOW")
        actions = plan.get("immediate_actions", [])
        if actions:
            for i, action in enumerate(actions, 1):
                with st.expander(f"#{i} — {action.get('action', '')}"):
                    st.markdown(f"**Why it matters:** {action.get('why', '')}")
                    st.markdown(f"**Time needed:** {action.get('time', '')}")
        else:
            st.info("No immediate actions found")

    # Tab 2 — Projects
    with tab2:
        st.subheader("🏗️ Projects to Build Next")
        projects = plan.get("projects_to_build", [])
        if projects:
            for proj in projects:
                priority = proj.get("priority", "medium")
                icon = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                with st.expander(f"{icon} {proj.get('project', '')}"):
                    st.markdown(f"**Skills gained:** {proj.get('skills_gained', '')}")
                    st.markdown(f"**Priority:** {priority.title()}")
        else:
            st.info("No projects recommended")

    # Tab 3 — Skills
    with tab3:
        st.subheader("📚 Skills to Learn Next")
        skills = plan.get("skills_to_learn", [])
        if skills:
            for skill in skills:
                with st.expander(f"📖 {skill.get('skill', '')}"):
                    st.markdown(f"**Where to learn:** {skill.get('resource', '')}")
                    st.markdown(f"**Time needed:** {skill.get('time', '')}")
        else:
            st.info("No skills recommended")

    # Tab 4 — Resume Fixes
    with tab4:
        st.subheader("📄 Resume Fixes")
        fixes = plan.get("resume_fixes", [])
        if fixes:
            for fix in fixes:
                st.markdown(f"✏️ {fix}")
        else:
            st.info("No resume fixes found")

        if results.get("resume"):
            st.divider()
            st.subheader("📊 Resume Analysis Details")
            resume = results["resume"]

            r1, r2, r3 = st.columns(3)
            r1.metric("Current Role",     resume.get("current_role", "N/A"))
            r2.metric("Years Experience", resume.get("years_experience", "N/A"))
            r3.metric("Resume Score",     f"{resume.get('overall_score', 0)}/100")

            st.markdown("**Technical Skills Found:**")
            tech = resume.get("technical_skills", [])
            st.write(", ".join(tech) if tech else "None found")

            st.markdown("**AI/ML Skills Found:**")
            ai = resume.get("ai_ml_skills", [])
            if ai:
                st.write(", ".join(ai))
            else:
                st.warning("No AI/ML skills on resume yet — add your current projects!")

            st.markdown("**Strengths:**")
            for s in resume.get("strengths", []):
                st.markdown(f"✅ {s}")

            st.markdown("**Gaps:**")
            for w in resume.get("weaknesses", []):
                st.markdown(f"⚠️ {w}")

    # Tab 5 — GitHub Fixes
    with tab5:
        st.subheader("🐙 GitHub Profile Fixes")
        github_fixes = plan.get("github_fixes", [])
        if github_fixes:
            for fix in github_fixes:
                st.markdown(f"✏️ {fix}")
        else:
            st.info("No GitHub fixes found")

        if results.get("github"):
            st.divider()
            st.subheader("📊 GitHub Analysis Details")
            github = results["github"]

            g1, g2, g3 = st.columns(3)
            g1.metric("GitHub Score",   f"{github.get('github_score', 0)}/100")
            g2.metric("Repos Analysed", github.get("repo_count", 0))
            g3.metric("Activity Level", github.get("activity_level", "Unknown").title())

            st.markdown("**AI Projects Found:**")
            ai_projs = github.get("ai_projects", [])
            if ai_projs:
                for p in ai_projs:
                    st.markdown(f"✅ {p}")
            else:
                st.warning("No AI projects on GitHub yet — push your 4 projects NOW!")

            st.markdown("**Main Languages:**")
            langs = github.get("main_languages", [])
            st.write(", ".join(langs) if langs else "None detected")

            st.markdown("**Profile Strengths:**")
            for s in github.get("profile_strengths", []):
                st.markdown(f"✅ {s}")

            st.markdown("**Profile Gaps:**")
            for g in github.get("profile_gaps", []):
                st.markdown(f"⚠️ {g}")
"""```

---

Save both files (`Ctrl+S`) and run:
```
cd C:\AI_Projects\portfolio_reviewer
streamlit run app.py
"""