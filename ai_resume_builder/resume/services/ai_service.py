"""
AI service for enhancing resume text and suggesting skills.
Uses OpenAI API if configured in settings, with intelligent rule-based fallbacks.
"""
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _call_openai(prompt, system_prompt="You are a professional resume writer and career coach."):
    """Call OpenAI API if key is set, else return None for fallback."""
    api_key = getattr(settings, 'OPENAI_API_KEY', '') or os.getenv('OPENAI_API_KEY', '')
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"OpenAI call failed: {e}")
        return None


def improve_summary(current_summary, job_title=""):
    """Improve or generate professional summary."""
    prompt = (
        f"Rewrite and enhance the following professional summary for a target role of '{job_title or 'Professional'}'. "
        f"Make it impactful, concise (3-4 sentences), and keyword-rich.\n\n"
        f"Current summary:\n{current_summary or 'Experienced professional seeking growth.'}"
    )

    ai_result = _call_openai(prompt)
    if ai_result:
        return ai_result

    # Fallback response
    role = job_title.strip() or "results-driven professional"
    if current_summary and len(current_summary.strip()) > 10:
        cleaned = current_summary.strip()
        return f"Dynamic and {role} with proven experience in delivering high-impact solutions. {cleaned} Track record of optimizing processes, driving cross-functional collaboration, and consistently achieving measurable performance outcomes."
    else:
        return f"Results-driven {role} with expertise in strategic execution, team leadership, and technical problem-solving. Demonstrated success in delivering high-quality outcomes in fast-paced environments. Adaptable professional skilled in process optimization and cross-functional communication."


def improve_experience(current_text, job_title=""):
    """Transform experience bullet points into action-oriented STAR format items."""
    prompt = (
        f"Transform the following work experience description for a '{job_title or 'Role'}' into 3-4 powerful, "
        f"action-verb-driven bullet points with quantified achievements.\n\n"
        f"Description:\n{current_text or 'Responsible for daily tasks and projects.'}"
    )

    ai_result = _call_openai(prompt)
    if ai_result:
        return ai_result

    # Fallback
    lines = [line.strip(' •-*') for line in (current_text or '').split('\n') if line.strip()]
    if not lines:
        lines = ["Managed daily operations and team deliverables", "Spearheaded process improvements to boost efficiency"]

    improved = []
    action_verbs = ["Spearheaded", "Architected", "Engineered", "Optimized", "Orchestrated", "Implemented"]
    for i, line in enumerate(lines):
        verb = action_verbs[i % len(action_verbs)]
        improved.append(f"• {verb} {line.lower() if not line.startswith(('http', 'API', 'SQL', 'AWS')) else line}, resulting in a 25% increase in operational efficiency.")
    return "\n".join(improved)


def suggest_skills(job_title="", current_skills=None):
    """Suggest relevant skills based on job title."""
    if current_skills is None:
        current_skills = []

    prompt = (
        f"List 10 relevant hard and soft skills for a '{job_title or 'Software Engineer'}'. "
        f"Return as a plain comma-separated list."
    )

    ai_result = _call_openai(prompt)
    if ai_result:
        skills = [s.strip() for s in ai_result.split(',') if s.strip()]
        return [s for s in skills if s.lower() not in [c.lower() for c in current_skills]]

    # Fallback database by keyword
    job_lower = (job_title or '').lower()
    skill_db = {
        'python': ['Python', 'Django', 'FastAPI', 'REST APIs', 'PostgreSQL', 'Docker', 'Git', 'Unit Testing', 'CI/CD'],
        'developer': ['JavaScript', 'React', 'Node.js', 'TypeScript', 'HTML5/CSS3', 'Git', 'RESTful APIs', 'SQL', 'Agile/Scrum'],
        'data': ['Python', 'SQL', 'Pandas', 'NumPy', 'Scikit-Learn', 'Tableau', 'PowerBI', 'Data Analysis', 'Machine Learning'],
        'manager': ['Project Management', 'Agile/Scrum', 'Stakeholder Management', 'Strategic Planning', 'Team Leadership', 'Budgeting', 'Jira'],
        'designer': ['Figma', 'UI/UX Design', 'Wireframing', 'Prototyping', 'User Research', 'Design Systems', 'Adobe XD'],
    }

    selected = []
    for key, skills in skill_db.items():
        if key in job_lower:
            selected.extend(skills)
            break

    if not selected:
        selected = ['Communication', 'Problem Solving', 'Project Management', 'Team Leadership', 'Strategic Planning', 'Time Management', 'Critical Thinking']

    return [s for s in selected if s.lower() not in [c.lower() for c in current_skills]]
