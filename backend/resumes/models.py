from django.db import models
from django.conf import settings
# Create your models here.
class Resume(models.Model):
    user=models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name="resumes"
    )
    file=models.FileField(upload_to="resumes/")
    original_filename=models.CharField(max_length=255)
    extracted_text=models.TextField(blank=True)
    skills=models.ManyToManyField("Skill",blank=True,related_name="resumes")
    uploaded_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    experience_years=models.FloatField(default=0,help_text="total years of professional experience")

    def __str__(self):
        return self.original_filename

class Skill(models.Model):
    name=models.CharField(max_length=100,unique=True)
    normalized_name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name