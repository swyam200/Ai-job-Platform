
def test_skill_gap_identifies_missing_skills(self):
        from resumes.services.job_matcher import calculate_skill_gap

        result = calculate_skill_gap(
            resume_skills=["Python", "Django"],
            job_skills=["Python", "Django", "React", "Docker"],
        )

        self.assertEqual(
            set(result["matched_skills"]),
            {"python", "django"},
        )
        self.assertEqual(
            set(result["missing_skills"]),
            {"react", "docker"},
        )
        self.assertEqual(result["skill_gap_count"], 2)

def test_matching_score_stays_between_zero_and_100(self):
        from resumes.services.job_matcher import calculate_skill_match

        result = calculate_skill_match(
            resume_skills=["Python", "Django", "SQL"],
            job_skills=["Python", "Django", "SQL"],
        )

        self.assertGreaterEqual(result["match_percentage"], 0)
        self.assertLessEqual(result["match_percentage"], 100)
