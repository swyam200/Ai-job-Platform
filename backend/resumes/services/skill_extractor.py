import re
from  resumes.skills_dictionary import SKILL_DICTIONARY

def extract_skills(text):
    if not text:
        return []
    text=text.lower()
    detected_skill=set()
    skill_sorted=sorted(SKILL_DICTIONARY.items(),key=lambda item:len(item[0]),reverse=True)
    for keyword,skill_name in skill_sorted:
        pattern=r"(?<!\n)"+re.escape(keyword)+r"(?<!\n)"
        if re.search(pattern,text):
            detected_skill.add(skill_name)
    return sorted(detected_skill)