from rest_framework import serializers
from .models import  Job,jobMatch  
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields=[
            "id",
            "title",
            "company",
            "location",
            "description",
            "required_skills",
            "salary_min",
            "salary_max",
            "experience_required",
            "job_type",
            "application_url",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields=[
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]
class JobMatchSerializer(serializers.ModelSerializer):
    job_title=serializers.CharField(source="job.title",read_only=True)
    company=serializers.CharField(source="job.company",read_only=True)

    class Meta:
        model=jobMatch
        fields=[
            "id",
            "resume",
            "job",
            "job_title",
            "company",
            "match_percentage",
            "skill_match_percentage",
            "experience_match_percentage",
            "semantic_match_percentage",
            "matched_skills",
            "missing_skills",
            "created_at",
            "updated_at"
        ]
        read_only_fields=fields