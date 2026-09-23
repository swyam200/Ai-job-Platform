from django.urls import path
from .views import ResumeListCreateView,ResumeDetailView,ResumeAnalyzeView,ResumeJobMatchView,ResumeAlljobsMatchView,ResumeSkillGapView

urlpatterns=[
    path("",ResumeListCreateView.as_view(),name="resume-list-create"),
    path("<int:pk>/",ResumeDetailView.as_view(),name="resume-detail"),
    path("<int:pk>/analyze/",ResumeAnalyzeView.as_view(),name="resume-analyze"),
    path("<int:pk>/match/<int:job_id>/",ResumeJobMatchView.as_view(),name="resume-job-match"),
    path("<int:pk>/match-all/",ResumeAlljobsMatchView.as_view(),name="resume-match-all"),
    path("<int:pk>/skill-gap/<int:job_id>/",ResumeSkillGapView.as_view(),name="resume-skill-gap"),
]