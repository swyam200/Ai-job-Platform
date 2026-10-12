import re
from resumes.services.semantic_matcher import calculate_semantic_similarity
from resumes.skills_aliases import SKILL_ALIASES
SKILL_WEIGHTS={
    "python":10,
    "django":10,
    "django rest framework":10,
    "react":8,
    "typescript":8,
    "sql":7,
    "docker":6,
    "kubernetes":5,
    "awa":5,
    "git":4,
     "javascript":8,
} 
def calculate_experience_match(resume_experience,job_experience):
    if not job_experience:
        return 100
    if resume_experience is None:
        return 0
    job_experience=job_experience.lower().strip()
    range_match=re.search(
        r"(\d+(?:\+)?)\s*-\s*(\d+(?:\.\d+)?)",job_experience
    )
    if range_match:
        minimum=float(range_match.group(1))
        maximum=float(range_match.group(2))
        if minimum<=resume_experience<=maximum:
            return 100
        if resume_experience<minimum:
           return 50
        return 90
    plus_match=re.search(r"(\d+(?:\.\d+)?)\s*\+",job_experience)
    if plus_match:
        minimum=float(plus_match.group(1))
        if resume_experience>=minimum:
            return 100
        return 50
    return 0
    
def calculate_skill_match(resume_skills,job_skills,resume_experience=None,job_experience=None):
    resume_skills={
        normalized_skill(skill)
        for skill in resume_skills
                }
    job_skills={
         normalized_skill(skill)
         for skill in job_skills
    }
    if not job_skills:
        experience_percentage=calculate_experience_match(resume_experience,job_experience)
        return {
            "match_percentage":experience_percentage*0.2,
            "skill_match_percentage":0,
            "experience_match_percentage":
            experience_percentage,"matched_skills":[],"missing_skills":[]
        }
    matched_skills=resume_skills.intersection(job_skills)
    missing_skills=job_skills-resume_skills
    total_score=0
    max_score=0
    for skill in job_skills:
        weight=SKILL_WEIGHTS.get(skill,10)
        max_score+=weight
        if skill in resume_skills:
            total_score+=weight
    skill_percentage=(
       total_score/max_score)*100
    experience_percentage=calculate_experience_match(resume_experience,job_experience)
    match_percentage=(skill_percentage*0.8+experience_percentage*0.2)
    return {
        "match_percentage":round(match_percentage,2),
        "skill_match_percentage":round(skill_percentage,2),
        "experience_match_percentage":experience_percentage,
        "matched_skills":sorted(matched_skills),
        "missing_skills":sorted(missing_skills)
    }
def normalized_skill(skill):
    skill=str(skill).lower().strip()
    return SKILL_ALIASES.get(skill,skill)
def calculate_skill_gap(resume_skills,job_skills):
    resume_skils={
        normalized_skill(skill)
        for skill in resume_skills
    }
    job_skills={
        normalized_skill(skill)
        for skill in job_skills
    }
    matched_skills=sorted(resume_skills & job_skills)
    missing_skills=sorted(job_skills-resume_skills)
    return{
        "matched_skills":matched_skills,
        "missing_skills":missing_skills,
        "skill_gap_count":len(missing_skills)
    }

def calculate_ai_match(
        resume_skills,
        job_skills,
        resume_experience,
        job_experience,
        resume_text,
        job_description
):
    skill_result=calculate_skill_match(resume_skills,job_skills,resume_experience,job_experience)
    semantic_score=calculate_semantic_similarity(resume_text,job_description)
    semantic_percentage=max(0,min(semantic_score*100,100))
    final_score=(skill_result["skill_match_percentage"]*0.50+semantic_percentage*0.30+skill_result["experience_match_percentage"]*0.20)
    return {
        "match_percentage":round(final_score,2),
        "skill_match_percentage":skill_result["skill_match_percentage"],
        "semantic_match_percentage":round(semantic_percentage,2),
        "experience_match_percentage":skill_result["experience_match_percentage"],
        "matched_skills":skill_result["matched_skills"],
        "missing_skills":skill_result["missing_skills"],
    }