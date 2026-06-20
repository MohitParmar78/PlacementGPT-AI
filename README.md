# 🚀 PlacementGPT-AI

### AI-Powered Resume Analysis, ATS Optimization & Interview Preparation Platform

PlacementGPT-AI is an end-to-end AI-powered career preparation platform designed to help students and job seekers improve their resumes, identify skill gaps, prepare for interviews, and track their readiness for target roles.

The platform leverages Large Language Models (LLMs), LangGraph multi-agent workflows, FastAPI, and Streamlit to deliver personalized resume analysis and interview coaching.

---

# 📌 Features

## 📄 Resume Analysis

* Upload resume PDF
* Automatic resume parsing
* Section extraction
* Candidate profile generation
* Resume statistics generation

### Extracted Sections

* Education
* Skills
* Projects
* Experience
* Certifications

---

## 🎯 ATS Optimization

Analyze resumes against role-specific requirements.

### ATS Analysis Includes

* ATS Score
* Resume Score
* Required Skills
* Matched Skills
* Missing Skills
* Keyword Match Percentage
* ATS Recommendations

---

## 🧠 Skill Gap Analysis

Compare resume skills with industry-required skills.

### Supported Roles

* Machine Learning Engineer
* Data Scientist
* Backend Developer

### Outputs

* Missing Skills
* Skill Gap Summary
* Personalized Recommendations

---

## ✨ Resume Improvement Engine

AI-powered resume enhancement suggestions.

### Improvement Categories

* Summary Improvements
* Project Improvements
* Experience Improvements
* Skill Improvements
* ATS Recommendations

---

## 🎤 AI Interview Preparation

Generate personalized interview questions based on:

* Resume Skills
* Resume Projects
* Experience
* Target Role

### Question Types

* Technical Questions
* Conceptual Questions
* Project-Based Questions
* Role-Specific Questions

---

## 🔄 Follow-Up Question Generation

Generate intelligent follow-up questions based on:

* Previous Question
* Candidate Answer
* Skill Area

Provides a more realistic interview experience.

---

## 📊 AI Interview Evaluation

Evaluate candidate responses using LLMs.

### Evaluation Includes

* Question-wise Scores
* Technical Score
* Communication Score
* Overall Score
* Strengths
* Weaknesses
* Improvement Suggestions
* Learning Roadmap

---

## 🛣 Personalized Learning Roadmap

Generate role-specific learning plans based on:

* Interview Performance
* Weak Skills
* Target Role

Example:

* Week 1: Python & SQL
* Week 2: Machine Learning
* Week 3: Deep Learning
* Week 4: Projects & Deployment

---

## 📑 PDF Assessment Reports

Automatically generate professional PDF reports containing:

* Interview Scores
* Question-wise Feedback
* Strengths
* Weaknesses
* Learning Roadmap
* Improvement Suggestions

---

# 🏗 System Architecture

```text
Resume Upload
      │
      ▼
Resume Parsing
      │
      ▼
Section Extraction
      │
      ▼
Skill Extraction
      │
      ▼
Candidate Profile
      │
      ▼
ATS Analysis
      │
      ▼
Skill Gap Analysis
      │
      ▼
Resume Improvement Agent
      │
      ▼
Question Generation
      │
      ▼
Interview Evaluation
      │
      ▼
Learning Roadmap
      │
      ▼
PDF Report Generation
```

---

# 🔄 LangGraph Multi-Agent Workflow

PlacementGPT-AI uses LangGraph to orchestrate multiple AI agents.

```text
Resume Text
      │
      ▼
Section Agent
      │
      ▼
Skill Agent
      │
      ▼
Profile Agent
      │
      ▼
ATS Agent
      │
      ▼
Skill Gap Agent
      │
      ▼
Resume Improvement Agent
      │
      ▼
Question Generation Agent
```

### Benefits of LangGraph

* Structured multi-agent orchestration
* State management between agents
* Modular architecture
* Easier scalability
* Better maintainability

---

# 🛠 Tech Stack

## Frontend

* Streamlit

## Backend

* FastAPI

## LLM

* Groq API
* Llama 3.3 70B

## AI Workflow

* LangGraph

## Machine Learning

* Scikit-Learn

## NLP

* Regular Expressions
* Resume Parsing

## PDF Generation

* ReportLab

---

# 📂 Project Structure

```text
PlacementGPT-AI
│
├── backend
│   ├── agents
│   ├── api
│   ├── config
│   ├── services
│   ├── workflows
│   └── reports
│
├── frontend
│
├── pages
│   ├── Resume_Analysis.py
│   ├── Interview.py
│   ├── Feedback.py
│   └── Dashboard.py
│
├── tests
│
├── uploads
│
└── requirements.txt
```

---

# 🚀 Installation

Clone repository:

```bash
git clone https://github.com/yourusername/PlacementGPT-AI.git

cd PlacementGPT-AI
```

Create environment:

```bash
conda create -n placementgpt python=3.10

conda activate placementgpt
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create `.env`

```env
GROQ_API_KEY=YOUR_API_KEY
```

---

# ▶ Run FastAPI Backend

```bash
uvicorn backend.api.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

# ▶ Run Streamlit Frontend

```bash
streamlit run Home.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# 🎯 Key Highlights

* Multi-Agent AI Architecture
* LangGraph Workflow Orchestration
* Resume Parsing Engine
* ATS Optimization
* Skill Gap Detection
* Resume Improvement Suggestions
* Personalized Interview Generation
* AI-Powered Evaluation
* Learning Roadmap Generation
* PDF Assessment Reports
* Full Stack AI Application

---

# 📈 Future Enhancements

* Cloud Database Integration
* Interview History Tracking
* Analytics Dashboard
* Resume Version Comparison
* Voice-Based Mock Interviews
* Deployment on AWS/GCP

---

# 👨‍💻 Author

**Mohit Rajput**

B.Tech Computer Science Engineering

Interested in:

* Machine Learning
* Deep Learning
* NLP
* Generative AI
* MLOps
* Backend Development

---

# ⭐ If you found this project useful

Please consider giving it a star on GitHub.
