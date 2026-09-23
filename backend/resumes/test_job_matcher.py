from django.test import SimpleTestCase
from resumes.services.job_matcher import(calculate_skill_match,normalized_skill)
class JobMatcherTest(SimpleTestCase):
    def test_skill_alias_normalization(self):
        self.assertEqual(normalized_skill("React.js"),"react")
        self.assertEqual(normalized_skill("DRF"),"django rest framework")
    def test_skill_matching_with_aliases(self):
        result=calculate_skill_match(resume_skills=["python","React.js","DRF"],job_skills=["python","react","django rest framework"])
        self.assertEqual(result["matched_skills"],["django rest framework","python","react"])
        self.assertEqual(result["missing_skills"],[])