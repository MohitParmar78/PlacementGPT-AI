<div align="center">

# ⚡ PlacementGPT-AI

**An AI-powered, multi-agent career preparation platform**

*Resume Intelligence · Semantic Skill Matching · AI Mock Interviews · LLM-Graded Feedback*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/langgraph)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Inference%20API-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/inference-api)

</div>

<br/>

> **Upload a resume. Pick a role. Get analyzed, quizzed, graded, and reported — end to end.**
> PlacementGPT-AI parses a resume, scores it against a live ATS model, finds the exact skill gaps for a target role, runs a personalised AI mock interview with follow-up questions, grades the answers like a strict FAANG interviewer, and exports everything as a PDF — with full history saved for next time.

<br/>

### Quick start

```bash
git clone https://github.com/MohitParmar78/PlacementGPT-AI.git
cd PlacementGPT-AI
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then add your GROQ_API_KEY

# Terminal 1 — backend
uvicorn backend.api.main:app --reload

# Terminal 2 — frontend
streamlit run app.py
```

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture & LangGraph Workflow](#️-architecture--langgraph-workflow)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running the Application](#️-running-the-application)
- [API Reference](#-api-reference)
- [Supported Roles](#-supported-roles)
- [Data Assets](#-data-assets)
- [Docker Deployment](#-docker-deployment)
- [Testing](#-testing)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🧭 Overview

PlacementGPT-AI takes a candidate from *"here's my resume"* to *"here's your interview-readiness report"* in one pipeline. A resume is parsed and scored, benchmarked against the real skill requirements of a target role, turned into a personalised mock interview, graded answer-by-answer by an LLM acting as a strict technical interviewer, and finally exported as a downloadable PDF — with every session persisted for later review.

Under the hood, resume analysis runs as a single **LangGraph** state machine that blends rule-based scoring, sentence-embedding similarity, and Groq-hosted **Llama 3.3 70B** calls — with four analysis agents (profile, stats, ATS, skill-gap) fanned out to run **in parallel** to keep latency down.

The app is split into two independently deployable services: a **Streamlit** multipage frontend and a **FastAPI** backend, connected over plain HTTP.

---

## 🎯 Features

<details open>
<summary><strong>📄 Resume Analysis</strong></summary>

Upload a PDF resume and the pipeline extracts and structures it end to end:

- **Text extraction** via PyMuPDF, with whitespace/line-noise cleanup
- **Section parsing** — education, skills, projects, experience, certifications (heading-based)
- **Skill extraction** — regex matching against a curated skill vocabulary
- **Candidate profile & stats** — skill counts, section-presence flags

</details>

<details>
<summary><strong>🎯 ATS Scoring</strong></summary>

| Output | What it tells you |
|--------|-------------------|
| Resume Score | Rule-based score (0–100) across skills, education, experience, projects, certifications |
| ATS Score | Hybrid score — semantic keyword match (60%) + resume score (40%), then refined by an LLM pass |
| Matched / Missing Skills | Semantic comparison against the target role's required-skill list, not just exact string matches |
| Keyword Match % | Percentage of required skills found (exactly or semantically) in the resume |
| Recommendations | Actionable, LLM-generated fixes |

</details>

<details>
<summary><strong>🧠 Semantic Skill Gap Analysis</strong></summary>

Resume skills and role requirements are embedded and compared with cosine similarity, so `"TensorFlow"` on a resume can correctly satisfy a requirement for `"Deep Learning"` frameworks — not just literal string matches. Supports **12 target roles** out of the box (see [Supported Roles](#-supported-roles)).

**Pluggable embedding backend** — the model that generates those embeddings is swappable via `EMBEDDING_BACKEND`, so the same matcher runs equally well on a laptop or a 512 MB free-tier host:

| Backend | How it works | Best for |
|---------|---------------|----------|
| `local` | Loads **Sentence-Transformers** (`all-MiniLM-L6-v2`) in-process | Local dev, or a deploy with enough RAM/build minutes for `torch` |
| `hf_api` | Calls the **Hugging Face Inference API** over HTTP using `HF_API_KEY` — no `torch` install, near-zero extra RAM, with automatic retry/backoff while the model "warms up" on HF's side | RAM-constrained hosts (e.g. Render's free tier) that still want real ML-based matching |
| `auto` *(default)* | Prefers `hf_api` if `HF_API_KEY` is set, otherwise falls back to `local` if it's installed | Letting the environment decide without touching code |

If neither backend is available or `ENABLE_SEMANTIC_MATCH=false`, the matcher transparently drops to a dependency-free **`difflib`** string-similarity comparison instead of erroring out — same `matched` / `missing` response shape either way, just a softer match quality.

</details>

<details>
<summary><strong>✨ Resume Improvement Suggestions</strong></summary>

A single Groq LLM call returns structured, section-by-section improvement ideas: summary rewrites, stronger project bullets, experience phrasing, skill-keyword additions, and ATS-specific formatting fixes.

</details>

<details>
<summary><strong>🎤 AI Mock Interview</strong></summary>

- **Personalised questions** generated from the *candidate's own* resume — skills, projects, experience, and target role — at Easy / Medium / Hard difficulty
- **Live countdown timer** widget embedded in the interview page
- **On-demand follow-up questions** — the interviewer probes deeper into a specific answer before moving on

</details>

<details>
<summary><strong>📊 Strict AI Interview Evaluation</strong></summary>

Every answer is graded by an LLM instructed to behave like a strict FAANG interviewer (empty, evasive, or "I don't know" answers are explicitly scored 0 — no credit for effort):

| Metric | Description |
|--------|-------------|
| Technical Score | Depth & accuracy across all answers |
| Communication Score | Clarity and structure of responses |
| Per-question Feedback | Score, critique, and an ideal answer for every question |
| Strengths / Weaknesses | At least two of each, generated per session |
| Learning Roadmap | A week-by-week study plan targeting the detected gaps |

</details>

<details>
<summary><strong>📑 PDF Assessment Reports</strong></summary>

One click on the Feedback page generates a downloadable PDF (via ReportLab) combining the resume analysis, ATS breakdown, skill gap, and full interview feedback into a single report.

</details>

<details>
<summary><strong>🗄️ Persistent Interview History</strong></summary>

Every evaluated interview is saved to a database (SQLite locally by default, or PostgreSQL in production — see [Environment Variables](#-environment-variables)) and browsable from the History page: scores, strengths/weaknesses, roadmap, and per-question feedback for every past session.

</details>

<details>
<summary><strong>⚖️ Resume Comparator</strong></summary>

Upload two resume versions for the same role and get a side-by-side breakdown: resume/ATS score deltas, detected-skill differences, missing-skill lists for each version, and an LLM-generated verdict on which version to submit — plus advice on combining the best of both.

</details>

---

## 🏗️ Architecture & LangGraph Workflow

PlacementGPT-AI runs as **two decoupled services**:

```
┌───────────────────────┐        HTTP (BACKEND_URL)       ┌────────────────────────────┐
│   Streamlit Frontend   │ ───────────────────────────────►│      FastAPI Backend       │
│   (app.py + pages/)    │◄─────────────────────────────── │   (backend/api/main.py)    │
└───────────────────────┘                                  └──────────────┬─────────────┘
                                                                            │
                                                        ┌───────────────────┼───────────────────┐
                                                        │                   │                   │
                                                 ┌──────▼──────┐    ┌───────▼───────┐    ┌───────▼───────┐
                                                 │  LangGraph   │    │  Groq LLM API  │    │  SQL Database  │
                                                 │ resume graph │    │ (Llama 3.3 70B)│    │ (SQLite/Postgres)│
                                                 └──────────────┘    └───────────────┘    └───────────────┘
```

Every `/analyze-resume` request is a single invocation of a **LangGraph `StateGraph`** built around a shared `PlacementState` TypedDict:

```
resume_text ──► [sections] ──► [skills] ──► [verification]
                                                  │
                                  ┌───────────────┴───────────────┐
                              is_valid                        not is_valid
                                  │                                │
                              [dispatch]                      [fallback]
                                  │                                │
                ┌─────────┬──────┴──────┬─────────┐                │
                ▼         ▼             ▼         ▼                │
           [profile]   [stats]       [ats]   [skill_gap]           │
                └─────────┴──────┬──────┴─────────┘                │
                                  ▼                                │
                            [aggregator]                           │
                                  │                                │
                            [improvements]                         │
                                  │                                │
                             [questions]                           │
                                  │                                │
                                  ▼                                ▼
                                 END ◄──────────────────────────────
```

### Node reference

| Node | Execution | Responsibility |
|------|-----------|-----------------|
| `sections` | Sequential | Splits the cleaned resume text into education / skills / projects / experience / certifications using heading-based line matching |
| `skills` | Sequential | Extracts a deduplicated skill list from the skills section by matching against `data/skills/skills.csv` |
| `verification` | Sequential | Flags the resume invalid if no skills, education, or experience text was parsed — guards against unreadable uploads |
| `dispatch` / `aggregator` | Fan-out / Fan-in | No-op sync nodes: `dispatch` triggers the four parallel branches; `aggregator` waits for all four before continuing |
| `profile` | **Parallel** | Builds a structured candidate profile (skills, total count, section-presence flags) |
| `stats` | **Parallel** | Computes resume statistics (skill count, education/experience/certification flags) |
| `ats` | **Parallel** | Computes `resume_score`, `ats_score`, a score breakdown, and ATS analysis — hybrid of rule-based scoring, semantic matching, and an LLM refinement pass |
| `skill_gap` | **Parallel** | Compares resume skills to the target role's required-skill matrix via sentence-embedding cosine similarity |
| `improvements` | Sequential | Single Groq call returning structured resume-improvement suggestions |
| `questions` | Sequential | Single Groq call generating personalised, resume-grounded interview questions at the chosen difficulty |
| `fallback` | Terminal | Returns safe zero-value defaults when `verification` fails, so the API never errors out on a bad upload |

### Why the parallel stage matters

Before fan-out, profile → stats → ATS → skill-gap ran as four sequential steps. `dispatch` now triggers all four simultaneously, and `aggregator` only lets the pipeline proceed once every branch has written its results back into the shared state — cutting pipeline latency without changing a single agent's logic.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (multipage app) |
| **Backend API** | FastAPI + Uvicorn |
| **Orchestration** | LangGraph (`StateGraph` with fan-out/fan-in) |
| **LLM** | Groq API — Llama 3.3 70B Versatile |
| **Semantic Matching** | Pluggable embedding backend — local **Sentence-Transformers** (`all-MiniLM-L6-v2`) or the **Hugging Face Inference API** (auto-selected via `EMBEDDING_BACKEND`) — with a dependency-free `difflib` fallback, compared via scikit-learn cosine similarity |
| **PDF Text Extraction** | PyMuPDF (`fitz`) |
| **PDF Report Generation** | ReportLab |
| **Database / ORM** | SQLAlchemy — SQLite by default, PostgreSQL-compatible via `DATABASE_URL` |
| **Data Handling** | Pandas |
| **Containerization** | Docker (backend service) |

---

## 📂 Project Structure

```
PlacementGPT-AI/
├── app.py                          # Streamlit entry point / landing page
│
├── pages/                          # Streamlit multipage app
│   ├── Resume_Analysis.py          # Upload & analyse a resume
│   ├── Interview.py                # Mock interview: questions, timer, follow-ups
│   ├── Feedback.py                 # Scores, feedback, roadmap, PDF report
│   ├── History.py                  # Browse past interview sessions
│   ├── Comparator.py                # Compare two resume versions
│   └── Dashboard.py                # Session-state summary dashboard
│
├── backend/
│   ├── agents/                     # Individual reasoning/scoring agents
│   │   ├── resume_agent.py         # Text cleaning, sectioning, profile & stats
│   │   ├── skill_agent.py          # Regex-based skill extraction
│   │   ├── scoring_agent.py        # Resume score + hybrid ATS score
│   │   ├── skill_gap_agent.py      # Semantic skill-gap analysis
│   │   ├── resume_improvement_agent.py
│   │   ├── question_agent.py       # Personalised question generation
│   │   ├── followup_question_agent.py
│   │   ├── interview_agent.py      # Strict LLM interview grading
│   │   ├── compare_agent.py        # Two-resume LLM comparison
│   │   └── report_agent.py         # PDF report generation
│   │
│   ├── api/
│   │   └── main.py                 # FastAPI routes
│   │
│   ├── config/
│   │   ├── settings.py             # Env var loading
│   │   └── role_loader.py          # Loads role → required-skills map
│   │
│   ├── database/
│   │   ├── db.py                   # Engine, session, Base
│   │   └── models.py               # InterviewSession ORM model
│   │
│   ├── models/
│   │   ├── embedding_model.py      # Singleton embedding client — local model, HF Inference API, or difflib fallback
│   │   └── semantic_matcher.py     # Cosine-similarity skill matcher
│   │
│   ├── services/
│   │   ├── file_service.py         # Uploaded-file persistence
│   │   ├── memory_service.py       # Interview save/fetch
│   │   └── resume_parser.py        # PDF → text
│   │
│   └── workflows/
│       └── interview_workflow.py   # LangGraph StateGraph definition
│
├── data/
│   ├── roles/role_skills.json      # Required-skill matrix, 12 roles
│   ├── skills/skills.csv           # Canonical skill vocabulary
│   └── questions/questions.json    # Static seed question bank (reference data)
│
├── tests/                          # Standalone module verification scripts
├── Dockerfile                      # Backend container image
├── .dockerignore
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (the Docker image uses 3.11)
- A [Groq API key](https://console.groq.com/) (free tier available)
- *(Optional)* A PostgreSQL connection string (e.g. [Neon](https://neon.tech/) or [Supabase](https://supabase.com/)) if you want persistent storage beyond local SQLite
- *(Optional)* A [Hugging Face access token](https://huggingface.co/settings/tokens) if you want ML-based semantic skill matching without installing `torch` locally

### 1. Clone the repository

```bash
git clone https://github.com/MohitParmar78/PlacementGPT-AI.git
cd PlacementGPT-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> `sentence-transformers` pulls in PyTorch. The first run will also download the `all-MiniLM-L6-v2` embedding model (~90 MB) automatically.

### 4. Configure environment variables

```bash
cp .env.example .env
# then edit .env and add your GROQ_API_KEY
# (optional: add HF_API_KEY / EMBEDDING_BACKEND to use the Hugging Face embedding backend — see below)
```

---

## 🔑 Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `GROQ_API_KEY` | **Yes** | — | Powers every LLM call: ATS refinement, resume improvements, question generation, follow-ups, interview grading, and resume comparison |
| `DATABASE_URL` | No | `sqlite:///./data/placementgpt.db` | Point this at a PostgreSQL URI to persist interview history in production; omit it to use the local SQLite file |
| `BACKEND_URL` | No (frontend only) | `http://localhost:8000` | Read by the Streamlit pages to locate the FastAPI backend — set this when the two services are deployed separately |
| `ENABLE_SEMANTIC_MATCH` | No | `true` | Master switch for embedding-based semantic skill matching. Set to `false` to force the lightweight `difflib` fallback everywhere — this is what the live Render deploy ships with by default |
| `EMBEDDING_BACKEND` | No | `auto` | Which embedding backend to use — `auto` (prefer the Hugging Face Inference API if `HF_API_KEY` is set, else fall back to a local model if installed), `hf_api` (force the HF Inference API), or `local` (force `sentence-transformers`, requires `torch`) |
| `HF_API_KEY` | No* | — | Hugging Face access token used to call the Inference API for embeddings instead of loading a model in-process — lets semantic matching run on low-RAM hosts without `torch`. *Required for the `hf_api` backend — get a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `HF_EMBEDDING_MODEL` | No | `sentence-transformers/all-MiniLM-L6-v2` | Which feature-extraction model the HF Inference API call requests embeddings from |
| `MODEL_NAME` | No | n/a — agents currently hardcode `llama-3.3-70b-versatile` | Present in `.env.example`/`settings.py`, reserved for future configurability |
| `OPENAI_API_KEY`, `CHROMA_DB_PATH` | No | — | Loaded in `settings.py` but not yet wired into any agent — reserved for future use |

> **Tip:** never commit `.env` — it's already excluded in `.gitignore`. That includes `HF_API_KEY`: treat it like any other secret and set it directly in your host's dashboard (e.g. Render's **Environment** tab) rather than in a tracked file.

---

## ▶️ Running the Application

The frontend and backend are two independent processes — run each in its own terminal.

### 1. Start the FastAPI backend

```bash
uvicorn backend.api.main:app --reload
```

- API → `http://127.0.0.1:8000`
- Interactive Swagger docs → `http://127.0.0.1:8000/docs`
- The `interview_sessions` table is created automatically on first launch — no manual migration needed.

### 2. Start the Streamlit frontend

```bash
streamlit run app.py
```

- App → `http://localhost:8501`

If the backend is deployed elsewhere, point the frontend at it before launching:

```bash
export BACKEND_URL="https://your-backend-host"
streamlit run app.py
```

---

## 📡 API Reference

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check — returns `{"message": "Backend Running"}` |
| `POST` | `/analyze-resume` | Upload a PDF (`resume`) + `target_role` + `difficulty`; runs the full LangGraph pipeline and returns sections, skills, stats, scores, skill gap, improvements, profile, and generated questions |
| `POST` | `/compare-resumes-llm` | Takes two already-analyzed resumes (`resume_a_data`, `resume_b_data`) and returns an LLM verdict, per-resume strengths, a comparison summary, and actionable advice |
| `POST` | `/evaluate-interview` | Grades a completed interview (question/skill/answer triples) with a strict LLM pass, persists the session, and returns full feedback |
| `POST` | `/generate-followup` | Generates one deeper follow-up question based on a candidate's answer |
| `GET` | `/history?limit=10` | Returns the most recent interview sessions from the database |

Full interactive documentation (request/response schemas) is available at `/docs` once the backend is running.

---

## 🎓 Supported Roles

`data/roles/role_skills.json` ships a required-skill matrix used by both the ATS scorer and the skill-gap agent, covering **12 target roles**:

`Machine Learning Engineer` · `Data Scientist` · `Data Analyst` · `Backend Developer` · `Frontend Developer` · `Full Stack Developer` · `Software Engineer` · `GenAI Engineer` · `Deep Learning Engineer` · `DevOps Engineer` · `Cloud Engineer` · `AI Research Engineer`

Adding a new role only requires adding a new key and skill list to that JSON file — no code changes needed.

---

## 🗃️ Data Assets

| File | Purpose |
|------|---------|
| `data/skills/skills.csv` | Canonical skill vocabulary used for regex-based extraction from the resume's skills section |
| `data/roles/role_skills.json` | Required-skill matrix for the 12 supported roles |
| `data/questions/questions.json` | A static, skill-grouped seed question bank bundled as reference data — interview questions are generated live per resume by the question agent, so this file isn't loaded at runtime today |

---

## 🐳 Docker Deployment

The included `Dockerfile` containerizes the **FastAPI backend only**, and is what powers the live backend on **[Render](https://render.com/)** today. The Streamlit frontend is designed to be deployed separately (e.g. Streamlit Community Cloud) and pointed at the container's public URL via `BACKEND_URL`.

```bash
docker build -t placementgpt-backend .
docker run -p 8000:8000 --env-file .env placementgpt-backend
```

Notable details baked into the image:

- Installs from **`requirements-render.txt`** — a lean dependency set that deliberately excludes `torch` / `sentence-transformers`, which together add 1–2 GB+ and enough runtime RAM to OOM a 512 MB free-tier instance the moment the embedding model loads. The full `requirements.txt` (with the ML stack) stays in the repo for local dev or a higher-RAM deploy
- Ships with `ENABLE_SEMANTIC_MATCH=false` baked in by default, so the container boots reliably on the free tier out of the box
- Real ML-based semantic matching still works from this lean image — set `HF_API_KEY` (plus `EMBEDDING_BACKEND=auto` and `ENABLE_SEMANTIC_MATCH=true`) on the host and `skill_gap_agent` calls the **Hugging Face Inference API** instead of loading a local model. Leave those unset and it transparently falls back to the `difflib`-based similarity check — see [Environment Variables](#-environment-variables)
- Respects an injected `PORT` environment variable (defaults to `8000`) — this is exactly how Render (and platforms like [Northflank](https://northflank.com/)) assign their own port at runtime

### Deploying to Render

1. Push the repo to GitHub, then create a new **Web Service** on Render pointed at it — Render auto-detects the `Dockerfile`
2. Under the service's **Environment** tab, add the variables from the table above: `GROQ_API_KEY` at minimum, `DATABASE_URL` for persistent Postgres history, and — for real semantic matching instead of the `difflib` fallback — `HF_API_KEY`, `EMBEDDING_BACKEND=auto`, and `ENABLE_SEMANTIC_MATCH=true`
3. Deploy, then point the Streamlit frontend's `BACKEND_URL` at the assigned `https://<your-service>.onrender.com` URL

> **Note:** free-tier Render services spin down on idle, so the first request after inactivity — and the first Hugging Face Inference API call, if that model needs to "warm up" — can take a few extra seconds. `embedding_model.py` already retries automatically on the HF side's `503` while the model loads.

---

## 🧪 Testing

`tests/` contains small, standalone verification scripts for the core modules (embedding, semantic matching, skill gap, the LangGraph workflow, follow-up questions, resume improvements, and PDF report generation). They exercise a function or class against a hard-coded example and print the result, rather than asserting via `pytest`. Run any of them directly:

```bash
python -m tests.test_matcher
python -m tests.test_langgraph
python -m tests.test_report
```

Use these as smoke tests during development, or as a starting point for a formal `pytest` suite.

---

## 🗺️ Roadmap

**Shipped**
- [x] Resume parsing, sectioning, and hybrid ATS scoring
- [x] Semantic skill-gap analysis across 12 target roles
- [x] AI mock interviews with a countdown timer and on-demand follow-ups
- [x] Strict LLM-based interview evaluation with per-question feedback and a learning roadmap
- [x] Downloadable PDF assessment reports
- [x] Persistent interview history (SQLite locally, PostgreSQL-ready for production)
- [x] Two-resume LLM-powered comparator
- [x] Parallel agent execution via LangGraph fan-out/fan-in
- [x] Resume validity gate with safe fallback defaults
- [x] Pluggable embedding backend — local Sentence-Transformers, the Hugging Face Inference API, or a dependency-free `difflib` fallback
- [x] Lean, ML-free Docker image deployed live on Render

**Potential next steps**
- [ ] Formal `pytest`-based automated test suite
- [ ] Analytics dashboard charting score trends over time
- [ ] Voice-based mock interviews
- [ ] Configurable LLM provider (wire up the currently unused `MODEL_NAME` / `OPENAI_API_KEY` settings)

---

## 🤝 Contributing

Contributions are welcome:

1. Fork the repository
2. Create a feature branch — `git checkout -b feature/your-feature`
3. Commit your changes with a clear message
4. Push and open a pull request

For larger changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This repository does not currently include a `LICENSE` file. If you plan to accept external contributions or reuse this code elsewhere, consider adding one — [MIT](https://choosealicense.com/licenses/mit/) is a common, permissive choice for projects like this.

---

## 👨‍💻 Author

**Mohit Rajput** — B.Tech, Computer Science Engineering
Interested in Machine Learning · Deep Learning · NLP · Generative AI · MLOps · Backend Development

[![GitHub](https://img.shields.io/badge/GitHub-MohitParmar78-181717?style=flat-square&logo=github)](https://github.com/MohitParmar78)

<div align="center">
<br/>

If PlacementGPT-AI helped you land your dream role — or just crack a tough interview — consider giving it a ⭐ on GitHub!

</div>