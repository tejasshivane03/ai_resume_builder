"""
ATS (Applicant Tracking System) calculation service.
Analyzes resume text against job description to compute ATS match score, missing keywords, and actionable suggestions.
"""
import re
from collections import Counter

# Standard stop words to ignore during keyword extraction
STOP_WORDS = set([
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with',
    'by', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'from', 'up', 'down', 'in', 'out', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'having', 'do', 'does', 'did', 'doing', 'i', 'you', 'he', 'she', 'it',
    'we', 'they', 'them', 'their', 'this', 'that', 'these', 'those', 'must',
    'ability', 'work', 'working', 'experience', 'years', 'required', 'preferred',
    'role', 'responsibilities', 'qualifications', 'position', 'job', 'description'
])


def analyze_ats(resume_text, job_description):
    """
    Perform detailed ATS analysis comparing resume_text with job_description.
    Returns a dictionary with:
    - score (0 - 100)
    - matched_keywords (list)
    - missing_keywords (list)
    - suggestions (list)
    - section_scores (dict)
    """
    if not resume_text or not job_description:
        return {
            'score': 0,
            'matched_keywords': [],
            'missing_keywords': [],
            'suggestions': ['Please provide both resume text and a job description for analysis.'],
            'section_scores': {'keywords': 0, 'formatting': 50, 'relevance': 0}
        }

    # Clean and tokenize
    resume_tokens = _extract_keywords(resume_text)
    job_tokens = _extract_keywords(job_description)

    # Word frequencies in JD
    jd_counts = Counter(job_tokens)
    top_jd_keywords = [word for word, count in jd_counts.most_common(40) if word not in STOP_WORDS and len(word) > 2]

    resume_tokens_set = set(resume_tokens)

    matched = []
    missing = []

    for kw in top_jd_keywords:
        if kw in resume_tokens_set:
            matched.append(kw.title())
        else:
            missing.append(kw.title())

    # Calculate Keyword Match Score (0 - 100)
    if top_jd_keywords:
        keyword_score = int((len(matched) / len(top_jd_keywords)) * 100)
    else:
        keyword_score = 50

    # Calculate Formatting Score
    formatting_score = _calculate_formatting_score(resume_text)

    # Calculate Overall Score (Weighted)
    overall_score = min(98, max(15, int(keyword_score * 0.7 + formatting_score * 0.3)))

    # Generate Actionable Suggestions
    suggestions = []

    if missing:
        top_missing = ", ".join(missing[:5])
        suggestions.append(f"Incorporate missing key terms: {top_missing}.")

    if len(resume_text.split()) < 250:
        suggestions.append("Your resume appears too short. Aim for at least 350-500 words with details.")

    if not re.search(r'\b(bullet|achieved|increased|managed|developed|led|improved|engineered|spearheaded)\b', resume_text, re.I):
        suggestions.append("Use strong action verbs (e.g., 'Spearheaded', 'Engineered', 'Optimized') to begin your experience bullet points.")

    if not re.search(r'\d+%', resume_text) and not re.search(r'\$\d+', resume_text):
        suggestions.append("Quantify your achievements with numbers, percentages, or dollar amounts (e.g., 'Increased performance by 30%').")

    if not suggestions:
        suggestions.append("Great job! Your resume matches the job description well.")

    return {
        'score': overall_score,
        'matched_keywords': list(set(matched)),
        'missing_keywords': list(set(missing)),
        'suggestions': suggestions,
        'section_scores': {
            'keyword_match': keyword_score,
            'formatting': formatting_score,
            'overall': overall_score
        }
    }


def _extract_keywords(text):
    """Extract clean lower-case words/terms from raw text."""
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = clean_text.split()
    return [w for w in words if len(w) > 2 and w not in STOP_WORDS]


def _calculate_formatting_score(text):
    """Check common ATS formatting best practices."""
    score = 70
    if '@' in text:
        score += 10
    if re.search(r'\b(education|experience|skills|projects|summary)\b', text, re.I):
        score += 10
    if len(text.split()) > 200:
        score += 10
    return min(100, score)
