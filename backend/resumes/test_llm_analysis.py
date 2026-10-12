
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from resumes.models import Resume, ResumeAnalysis


User = get_user_model()


class ResumeLLMAnalysisTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a resume without uploading a real PDF.
        self.resume = Resume.objects.create(
            user=self.user,
            original_filename="test_resume.pdf",
            extracted_text="Python Django developer with REST API experience."
        )

        self.url = (
            f"/api/resumes/{self.resume.id}/llm-analysis/"
        )

        self.analysis_data = {
            "summary": "Python Django developer.",
            "strengths": ["Python", "Django"],
            "weaknesses": ["Limited testing experience"],
            "suggested_skills": ["Docker"],
            "improvement_tips": ["Add project outcomes."]
        }

    def test_get_analysis_not_found(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_get_saved_analysis(self):
        ResumeAnalysis.objects.create(
            resume=self.resume,
            **self.analysis_data
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["analysis"]["summary"],
            self.analysis_data["summary"]
        )

    @patch(
        "resumes.views.analyze_resume"
    )
    def test_post_creates_analysis(self, mock_analyze):
        mock_analyze.return_value = self.analysis_data

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ResumeAnalysis.objects.filter(
                resume=self.resume
            ).exists()
        )
        mock_analyze.assert_called_once_with(
            self.resume.extracted_text
        )
