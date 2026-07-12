import json
from groq import Groq
from backend.config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_resume_comparison(target_role, resume_a_data, resume_b_data):
    """
    Generate an LLM-based side-by-side comparison of two resumes.
    """
    prompt = f"""
You are an expert technical recruiter and ATS evaluator.
Your task is to compare two resumes side-by-side for the target role: {target_role}

### Resume A Data:
Skills: {json.dumps(resume_a_data.get('profile', {}).get('skills', []))}
ATS Score: {resume_a_data.get('ats_score', 0)}
Resume Score: {resume_a_data.get('resume_score', 0)}

### Resume B Data:
Skills: {json.dumps(resume_b_data.get('profile', {}).get('skills', []))}
ATS Score: {resume_b_data.get('ats_score', 0)}
Resume Score: {resume_b_data.get('resume_score', 0)}

Compare the two resumes and provide a detailed analysis. Which one is better suited for the {target_role} role and why? What are the trade-offs?

Return ONLY valid JSON in the following format:
{{
    "verdict": "Resume A is better / Resume B is better / Tie",
    "resume_a_strengths": ["..."],
    "resume_b_strengths": ["..."],
    "comparison_summary": "A detailed paragraph explaining the trade-offs and reasoning behind the verdict.",
    "actionable_advice": "What should the candidate do to improve the losing resume, or combine the best of both?"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        print(f"Error in LLM comparison: {e}")
        return {
            "verdict": "Could not determine",
            "resume_a_strengths": [],
            "resume_b_strengths": [],
            "comparison_summary": "An error occurred while generating the LLM comparison. Please check your API key and rate limits.",
            "actionable_advice": ""
        }
