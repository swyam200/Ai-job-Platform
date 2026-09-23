from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    email=models.EmailField(unique=True)
def __str__(self):
    return self.username
# Create your models here.
class CandidateProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    full_name=models.CharField(max_length=150)
    phone=models.CharField(max_length=15,blank=True)
    location=models.CharField(max_length=100,blank=True)
    bio=models.TextField(blank=True)
    Skill=models.TextField(blank=True)
    education=models.TextField(blank=True)
    experience=models.TextField(blank=True)
    resume=models.FileField(upload_to="resumes/",blank=True,null=True)
    Created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
