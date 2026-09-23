from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services.skill_extractor import extract_skills
from jobs.models import Job,jobMatch
from .services.job_matcher import calculate_skill_match,calculate_skill_gap
from .models import Resume,Skill
from .serializers import ResumeSerializer
class ResumeListCreateView(generics.ListCreateAPIView):
      serializer_class=ResumeSerializer
      permission_classes=[IsAuthenticated]
      def get_queryset(self):
            return Resume.objects.filter(user=self.request.user)
      def perform_create(self,serializer):
            file=self.request.FILES["file"]
            from .utils import extract_text_from_pdf
            extracted_text=extract_text_from_pdf(file)
            serializer.save(
                  user=self.request.user,
                  original_filename=file.name,
                  extracted_text=extracted_text
            )
# Create yur views here.
class ResumeDetailView(generics.RetrieveDestroyAPIView):
      serializer_class=ResumeSerializer
      permission_classes=[IsAuthenticated]

      def  get_queryset(self):
            return Resume.objects.filter(user=self.request.user)

class ResumeAnalyzeView(generics.GenericAPIView):
      serializer_class=ResumeSerializer
      permission_classes=[IsAuthenticated]

      def get_queryset(self):
            return Resume.objects.filter(user=self.request.user)
      def post(self,request,pk):
            resume=self.get_object()
            skills=extract_skills(resume.extracted_text)
            resume.skills.clear()
            for skill_name in skills:
                  normalized_name=skill_name.lower()
                  skill,created=Skill.objects.get_or_create(normalized_name=normalized_name,defaults={"name":skill_name})
                  resume.skills.add(skill)
            return Response({
                  "resume_id":resume.id,
                  "skills":[
                        {
                        "id":skill.id,
                        "name":skill.name,
                        "normalized_name":skill.normalized_name
                        }for skill in resume.skills.all()
                  ],
                  "message":"Resume analyzed successfully"
            })

class ResumeJobMatchView(generics.GenericAPIView):
      permission_classes=[IsAuthenticated]

      def get_queryset(self):
            return Resume.objects.filter(user=self.request.user)

      def post(self,request,pk,job_id):
            resume=self.get_object()

            try:
                job=Job.objects.get(id=job_id)
            except job.DoesNotExist:
                  return Response({"error":"job not found"},status=404)
            resume_skills=list(resume.skills.values_list("name",flat=True))
            result=calculate_skill_match(resume_skills,job.required_skills,resume_experience=resume.experience_years,job_experience=job.experience_required)
            jobMatch.objects.update_or_create(
                  resume=resume,
                  job=job,
                  defaults={
                        "match_percentage":result["match_percentage"],
                        "skill_match_percentage":result["skill_match_percentage"],
                        "experience_match_percentage":result["experience_match_percentage"],
                        "matched_skills":result[ "matched_skills"],
                        "missing_skills":result["missing_skills"],
                  }
            )
            return Response({
                  "resume_id":resume.id,
                  "job_id":job.id,
                  "job_title":job.title,
                  "company":job.company,
                  **result
            })
class ResumeAlljobsMatchView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    def get(self,request,pk):
          resume=self.get_object()
          resume_skill=list(resume.skills.values_list("name",flat=True))
          jobs=Job.objects.all()
          result=[]
          for job in jobs:
                match=calculate_skill_match(resume_skill,job.required_skills,resume_experience=resume.experience_years,job_experience=job.experience_required)
                result.append({
                      "job_id":job.id,
                      "job_title":job.title,
                      "company":job.company,
                      **match
                })
                result.sort(key=lambda x:x["match_percentage"],reverse=True)
          return Response({
                "resume_id":resume.id,
                "total_jobs":len(result),
                "jobs":result
          })

class ResumeSkillGapView(generics.GenericAPIView):
      permission_classes=[IsAuthenticated]
      def get_queryset(self):
            return Resume.objects.filter(user=self.request.user)
      def get(self,request,pk,job_id):
            resume=self.get_object()
            try:
                  job=Job.objects.get(id=job_id)
            except job.DoesNotExist:
                  return Response({"error":"job not found"},status=404)
            resume_skills={
                  skill.lower().strip()
                  for skill in resume.skills.values_list(
                        "name",
                        flat=True
                  )
            }
            job_skills={
                  skill.lower().strip()
                  for skill in job.required_skills
            }
            matched_skills=sorted(resume_skills.intersection(job_skills))
            missing_skills=sorted(job_skills-resume_skills)
            return Response({
                  "resume_id":resume.id,
                  "job_id":job.id,
                  "job_title":job.title,
                  "company":job.company,
                  "matched_skills":matched_skills,
                  "missing_skills":missing_skills,
                  "skill_gap_count":len(missing_skills)
            })
                               
