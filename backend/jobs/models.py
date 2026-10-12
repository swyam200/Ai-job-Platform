from django.db import models
from django.conf import settings

class Job(models.Model):
    title=models.CharField(max_length=255)
    company=models.CharField(max_length=255)
    location=models.CharField(max_length=255,blank=True)
    description=models.TextField()
    required_skills=models.JSONField(default=list,blank=True)
    salary_min=models.PositiveIntegerField(null=True,blank=True)
    salary_max=models.PositiveIntegerField(null=True,blank=True)
    experience_required=models.CharField(max_length=100,blank=True)
    job_type=models.CharField(max_length=50,blank=True)
    application_url=models.URLField(blank=True)
    created_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="jobs"
    )
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}-{self.company}"

class jobMatch(models.Model):
    resume=models.ForeignKey("resumes.Resume",on_delete=models.CASCADE,related_name="resume_matches")
    job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name="resume_matches")
    match_percentage=models.FloatField()
    skill_match_percentage=models.FloatField(default=0)
    experience_match_percentage=models.FloatField(default=0)
    semantic_match_percentage=models.FloatField(default=0)
    matched_skills=models.JSONField(default=list,blank=True)
    missing_skills=models.JSONField(default=list,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=("resume","job")
    def __str__(self):
        return f"{self.resume}-{self.job}-{self.match_percentage}%"

# Create your models here.
