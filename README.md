<div align="center">

<h1>⚡ PlacementGPT-AI</h1>

<p><strong>An end-to-end, AI-powered career preparation platform</strong><br/>
<em>LangGraph · Groq · FastAPI · Streamlit · Neon DB</em></p>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-MultiAgent-F7931E?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/langgraph)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-6C1FFF?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![Neon](https://img.shields.io/badge/Neon-PostgreSQL-00E5C9?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

> 🚀 **Upload your resume. Pick a role. Let AI do the rest.**
> PlacementGPT-AI analyses your resume, detects skill gaps, coaches you through mock interviews, compares multiple resume versions, and stores your full interview history in a persistent cloud database — all in one sleek Streamlit app.

<br/>

---

</div>

## 📌 Table of Contents

- [✨ What's New](#-whats-new)
- [🎯 Core Features](#-core-features)
- [🗄️ Persistent Storage — Neon DB](#️-persistent-storage--neon-db)
- [📊 Resume Comparator](#-resume-comparator)
- [🏗️ System Architecture](#️-system-architecture)
- [🔄 LangGraph Multi-Agent Workflow](#-langgraph-multi-agent-workflow)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [🔑 Environment Variables](#-environment-variables)
- [▶️ Running the App](#️-running-the-app)
- [👨‍💻 Author](#-author)

---

## ✨ What's New

| # | Feature | Description |
|---|---------|-------------|
| 🆕 | **Persistent Interview History** | All interview sessions are saved to a serverless **Neon PostgreSQL** database — revisit scores, questions, and feedback anytime |
| 🆕 | **Resume Comparator** | Upload two versions of your resume and get a side-by-side AI analysis highlighting improvements, regressions, and ATS score delta |
| ⚡ | **Cloud-native Storage** | Zero-config Neon DB integration — no self-hosted Postgres needed |
| ⚡ | **Parallel Agent Execution** | Profile, Stats, ATS, and Skill Gap agents now run concurrently via LangGraph fan-out — cutting pipeline latency by up to 4× |
| 🛡️ | **Resume Validity Gate** | A verification node short-circuits the pipeline on unreadable uploads, returning safe defaults instantly instead of propagating errors |

---

## 🎯 Core Features

<details>
<summary><strong>📄 Resume Analysis</strong></summary>

Upload any PDF resume and PlacementGPT-AI immediately extracts and structures every section:

- **Automatic parsing** — education, skills, projects, experience, certifications
- **Candidate profile generation** — synthesises a structured profile from raw text
- **Resume statistics** — keyword density, section completeness score, readability metrics

</details>

<details>
<summary><strong>🎯 ATS Optimization</strong></summary>

Know exactly how an Applicant Tracking System reads your resume before a recruiter ever sees it:

| Output | What it tells you |
|--------|-------------------|
| ATS Score | Overall machine-readability score (0–100) |
| Resume Score | Human-readability & content quality |
| Matched Skills | Skills present in both resume and JD |
| Missing Skills | Keywords the ATS expects but can't find |
| Keyword Match % | Exact percentage overlap with role requirements |
| ATS Recommendations | Actionable fixes to boost the score |

</details>

<details>
<summary><strong>🧠 Skill Gap Analysis</strong></summary>

Compare your current skill-set against what the industry actually demands for your target role.

**Supported roles (expanding):**
- Machine Learning Engineer
- Data Scientist
- Backend Developer

**Output:** missing skills list · gap summary · personalised learning recommendations

</details>

<details>
<summary><strong>✨ Resume Improvement Engine</strong></summary>

AI-generated enhancement suggestions across every section:

- Summary rewrite ideas
- Stronger project bullet points
- Experience phrasing improvements
- Skill keyword additions
- ATS-specific formatting recommendations

</details>

<details>
<summary><strong>🎤 AI Mock Interview</strong></summary>

Get personalised interview questions generated from *your* resume, not a generic question bank:

- **Technical questions** — based on your listed skills
- **Conceptual questions** — core theory for your target role
- **Project-based questions** — deep dives into *your own* projects
- **Role-specific questions** — what top companies ask for that position

**Follow-up generation** — answers a follow-up question based on your response, simulating a real back-and-forth interview.

</details>

<details>
<summary><strong>📊 AI Interview Evaluation</strong></summary>

Submit your answers and receive a detailed LLM-powered evaluation:

| Metric | Description |
|--------|-------------|
| Technical Score | Depth & accuracy of your answers |
| Communication Score | Clarity, structure, confidence |
| Per-question Scores | Granular breakdown per question |
| Strengths | What you did well |
| Weaknesses | Areas needing improvement |
| Learning Roadmap | Week-by-week study plan to close gaps |

</details>

<details>
<summary><strong>🛣️ Personalised Learning Roadmap</strong></summary>

Generates a structured, week-by-week roadmap based on your interview performance and target role. Example:

```
Week 1 → Python fundamentals & SQL
Week 2 → Core Machine Learning algorithms
Week 3 → Deep Learning & model deployment
Week 4 → End-to-end project & system design
```

</details>

<details>
<summary><strong>📑 PDF Assessment Reports</strong></summary>

Every interview session can be exported as a polished PDF report containing:

- Interview scores (technical + communication + overall)
- Question-by-question feedback
- Strengths & improvement areas
- Personalised learning roadmap

</details>

---

## 🗄️ Persistent Storage — Neon DB

PlacementGPT-AI now uses [Neon](https://neon.tech/) — a serverless, autoscaling PostgreSQL platform — to persist all interview data across sessions.

### What gets stored

```
interviews
├── session_id          (UUID, primary key)
├── candidate_name
├── target_role
├── created_at          (timestamp)
├── technical_score
├── communication_score
├── overall_score
├── questions           (JSONB)
├── answers             (JSONB)
├── feedback            (JSONB)
└── learning_roadmap    (JSONB)
```

### Why Neon?

| Feature | Benefit |
|---------|---------|
| Serverless | No server to manage; scales to zero when idle |
| Branching | Create instant DB branches for dev/test |
| Postgres-compatible | Use any standard Postgres client or ORM |
| Free tier | Generous free tier — perfect for side projects |

### Setup

1. Create a free project at [neon.tech](https://neon.tech/)
2. Copy your connection string
3. Add it to `.env` (see [Environment Variables](#-environment-variables))

The schema is auto-created on first run — no migrations needed.

---

## 📊 Resume Comparator

The **Resume Comparator** is a brand-new module that lets you upload two resume versions and get a comprehensive side-by-side analysis.

### How it works

```
Resume V1 (PDF)  ──┐
                    ├──► LLM Comparison Agent ──► Structured Diff Report
Resume V2 (PDF)  ──┘
```

### What you get

- **Section-level diff** — which sections improved, degraded, or stayed the same
- **ATS score delta** — quantified improvement in machine-readability
- **New skills detected** — skills added in V2 that weren't in V1
- **Removed content warnings** — flags important content dropped from V1
- **Overall recommendation** — which version to submit and why
- **Keyword density comparison** — side-by-side keyword analysis per section

### Use cases

- Before/after resume editing sessions
- Tailoring a resume for different roles
- A/B testing two resume formats

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                   │
│  Resume Upload │ Interview UI │ History │ Comparator     │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP (REST)
┌───────────────────────────▼─────────────────────────────┐
│                      FastAPI Backend                     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │            LangGraph Agent Orchestrator          │    │
│  │                                                  │    │
│  │  Section Agent → Skill Agent → Profile Agent    │    │
│  │       → ATS Agent → Skill Gap Agent             │    │
│  │       → Improvement Agent → Question Agent      │    │
│  │       → Evaluation Agent → Roadmap Agent        │    │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────▼───────────────────────────┐   │
│  │          Groq API  (Llama 3.3 70B)               │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌───────────────────┐   ┌──────────────────────────┐   │
│  │   Resume Comparator│   │      PDF Report Gen      │   │
│  │      Module        │   │       (ReportLab)        │   │
│  └───────────────────┘   └──────────────────────────┘   │
└───────────────────────────┬─────────────────────────────┘
                            │
          ┌─────────────────▼──────────────────┐
          │         Neon DB (PostgreSQL)        │
          │  Interview History · Session Data   │
          └─────────────────────────────────────┘
```

---

## 🔄 LangGraph Multi-Agent Workflow

PlacementGPT-AI uses a directed LangGraph `StateGraph` with a shared `PlacementState` TypedDict. The pipeline is split into three stages: a **sequential parse stage**, a **parallel analysis stage**, and a **sequential generation stage**. A validity gate after parsing short-circuits bad uploads before any expensive LLM work begins.

### Full Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       STAGE 1 — PARSE                          │
│                                                                 │
│   Resume Text ──► [ Section Agent ] ──► [ Skill Agent ]         │
│                                               │                 │
└───────────────────────────────────────────────┼─────────────────┘
                                                │
                                    ┌───────────▼────────────┐
                                    │   Verification Node    │
                                    │  checks sections +     │
                                    │  skills are non-empty  │
                                    └───────────┬────────────┘
                                                │
                            ┌───────────────────┴──────────────────┐
                            │ conditional_edges (check_validity)    │
                            │                                       │
                      "valid"▼                               "invalid"▼
              ┌─────────────────────┐                 ┌──────────────────────┐
              │   Dispatch Node     │                 │    Fallback Node      │
              │  (fan-out trigger)  │                 │  safe zero-defaults  │
              └──┬──────┬──────┬───┘                 └──────────┬───────────┘
                 │      │      │      │                          │
┌────────────────▼──────▼──────▼──────▼──────────────┐         │
│              STAGE 2 — PARALLEL ANALYSIS            │         │
│                                                     │         │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────┐  │         │
│  │ Profile Agent│  │Stats Node│  │  ATS Agent   │  │         │
│  │ (profile)    │  │ (stats)  │  │ (ats_score,  │  │         │
│  │              │  │          │  │  resume_score│  │         │
│  │              │  │          │  │  breakdown,  │  │         │
│  │              │  │          │  │  ats_analysis│  │         │
│  └──────┬───────┘  └────┬─────┘  └──────┬───────┘  │         │
│         │               │               │           │         │
│  ┌──────▼───────────────▼───────────────▼────────┐  │         │
│  │              Skill Gap Agent                  │  │         │
│  │            (skill_gap result)                 │  │         │
│  └──────────────────────┬────────────────────────┘  │         │
│                         │  all four write back       │         │
│                         │  to shared PlacementState  │         │
└─────────────────────────┼───────────────────────────┘         │
                          │                                      │
              ┌───────────▼───────────┐                         │
              │    Aggregator Node    │◄────────────────────────┘
              │  (fan-in sync point)  │
              └───────────┬───────────┘
                          │
┌─────────────────────────▼────────────────────────────────────┐
│                    STAGE 3 — GENERATE                        │
│                                                              │
│  [ Improvement Agent ] ──► [ Question Agent ] ──► [ END ]   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Node Reference

| Node | Type | Responsibility |
|------|------|----------------|
| `sections` | Sequential | Parses resume text into structured sections (education, skills, experience, projects, certifications) |
| `skills` | Sequential | Extracts a deduplicated skill list from the skills section |
| `verification` | Sequential | Validates that at least one meaningful field was extracted |
| `dispatch` | Fan-out | Dummy node that triggers all four parallel branches simultaneously |
| `fallback` | Terminal | Returns zero-value defaults when the resume is unreadable — pipeline exits safely |
| `profile` | **Parallel** | Builds a structured candidate profile from sections + skills |
| `stats` | **Parallel** | Generates resume statistics (skill count, section presence flags) |
| `ats` | **Parallel** | Calculates ATS score, resume score, score breakdown, and ATS recommendations against the target role |
| `skill_gap` | **Parallel** | Loads role skill matrix, compares to resume skills, returns missing + required skills |
| `aggregator` | Fan-in | Dummy sync node — waits for all four parallel branches to write state before continuing |
| `improvements` | Sequential | Generates LLM-powered resume improvement suggestions per section |
| `questions` | Sequential | Generates personalised interview questions by difficulty level |

### State Schema

All nodes read from and write back to a single shared `PlacementState` TypedDict:

```python
class PlacementState(TypedDict, total=False):
    # Inputs
    resume_text: str
    target_role: str
    difficulty: str          # "Easy" | "Medium" | "Hard"

    # Parse stage outputs
    sections: dict           # {education, skills, experience, projects, certifications}
    skills: list             # deduplicated skill tokens
    is_valid: bool           # set by verification node

    # Parallel stage outputs
    profile: dict
    stats: dict
    resume_score: int
    ats_score: int
    score_breakdown: dict
    ats_analysis: dict
    skill_gap: dict

    # Generation stage outputs
    resume_improvements: dict
    questions: list
```

### Why the parallel stage matters

Before this redesign, Profile → Stats → ATS → Skill Gap ran sequentially, making 4 back-to-back LLM/compute calls. Now LangGraph fans out from the `dispatch` node and all four agents execute concurrently, writing their results into the shared state independently. The `aggregator` fan-in ensures downstream nodes only proceed once every branch has completed.

**Why LangGraph?**
- Explicit, auditable state transitions — every field change is traceable
- Native fan-out / fan-in edges for true parallel execution
- Conditional routing without ad-hoc if/else spaghetti
- Shared `TypedDict` state prevents agents from stepping on each other
- Fallback path keeps the app responsive on bad input

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **AI Orchestration** | LangGraph |
| **LLM** | Groq API · Llama 3.3 70B |
| **Database** | Neon DB (serverless PostgreSQL) |
| **ML** | Scikit-Learn |
| **NLP / Parsing** | Custom regex-based resume parser |
| **PDF Generation** | ReportLab |
| **PDF Reading** | PyPDF2 / pdfplumber |

---

## 📂 Project Structure

```
PlacementGPT-AI/
│
├── backend/
│   ├── agents/               # Individual LangGraph agents
│   │   ├── section_agent.py
│   │   ├── skill_agent.py
│   │   ├── ats_agent.py
│   │   ├── skill_gap_agent.py
│   │   ├── improvement_agent.py
│   │   ├── question_agent.py
│   │   └── evaluation_agent.py
│   │
│   ├── api/                  # FastAPI route handlers
│   │   └── main.py
│   │
│   ├── config/               # Settings & env loading
│   ├── db/                   # Neon DB connection & queries
│   │   ├── connection.py
│   │   └── interview_store.py
│   │
│   ├── services/             # Business logic layer
│   ├── workflows/            # LangGraph workflow definitions
│   └── reports/              # PDF report generation (ReportLab)
│
├── pages/
│   ├── Resume_Analysis.py    # Upload & analyse resume
│   ├── Interview.py          # Run mock interview session
│   ├── Feedback.py           # View AI evaluation & scores
│   ├── History.py            # 🆕 Browse past interview sessions
│   └── Comparator.py         # 🆕 Compare two resume versions
│
├── data/                     # Role skill matrices & reference data
├── tests/                    # Unit & integration tests
│
├── app.py                    # Streamlit entry point
├── .env.example              # Environment variable template
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/) (free tier available)
- A [Neon DB](https://neon.tech/) project (free tier available)

### 1. Clone the repository

```bash
git clone https://github.com/MohitParmar78/PlacementGPT-AI.git
cd PlacementGPT-AI
```

### 2. Create a virtual environment

```bash
# Using conda (recommended)
conda create -n placementgpt python=3.10
conda activate placementgpt

# Or using venv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Then edit .env with your keys (see below)
```

---

## 🔑 Environment Variables

```env
# ── LLM ──────────────────────────────────────────────────────
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile

# ── Database (Neon DB) ───────────────────────────────────────
# Get this from your Neon project dashboard → Connection Details
DATABASE_URL=postgresql://user:password@ep-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

> **Tip:** Never commit `.env` to version control. The `.gitignore` already excludes it.

---

## ▶️ Running the App

### Start the FastAPI backend

```bash
uvicorn backend.api.main:app --reload
```

API available at: `http://127.0.0.1:8000`  
Swagger docs at: `http://127.0.0.1:8000/docs`

### Start the Streamlit frontend

```bash
streamlit run app.py
```

App available at: `http://localhost:8501`

---

## 🗺️ Roadmap

- [x] Resume parsing & ATS analysis
- [x] Skill gap detection
- [x] AI mock interview & evaluation
- [x] PDF report generation
- [x] **Persistent interview history (Neon DB)**
- [x] **Resume comparator**
- [x] **Parallel agent execution (LangGraph fan-out/fan-in)**
- [x] **Resume validity gate with safe fallback**
- [ ] Analytics dashboard — visualise progress over time
- [ ] Voice-based mock interviews

---

## 👨‍💻 Author

**Mohit Rajput**  
B.Tech Computer Science Engineering

Passionate about Machine Learning · Deep Learning · NLP · Generative AI · MLOps · Backend Development

[![GitHub](https://img.shields.io/badge/GitHub-MohitParmar78-181717?style=flat-square&logo=github)](https://github.com/MohitParmar78)

---

<div align="center">

If PlacementGPT-AI helped you land your dream role (or just crack a tough interview), consider giving it a ⭐ on GitHub — it means a lot!

</div>
