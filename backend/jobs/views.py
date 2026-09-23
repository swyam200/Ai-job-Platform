from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Job,jobMatch
from .serializers import JobSerializer,JobMatchSerializer

class JobListCreateView(generics.ListCreateAPIView):
    queryset=Job.objects.all()
    serializer_class=JobSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        queryset=Job.objects.all().order_by("-created_at")
        search=self.request.query_params.get("search")
        location=self.request.query_params.get("location")
        job_type=self.request.query_params.get("job_type")
        skill=self.request.query_params.get("skill")
        if search:
            queryset=queryset.filter(title__icontains=search)| queryset.filter(company__icontains=search)
        if location:
            queryset=queryset.filter(location__icontains=location)
        if job_type:
            queryset=queryset.filter(job_type__iexact=job_type)
        if skill:
            queryset=queryset.filter(required_skills__icontains=skill)
        return queryset

    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=JobSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Job.objects.all()
class JobMatchListView(generics.ListAPIView):
    serializer_class=JobMatchSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return jobMatch.objects.filter(resume__user=self.request.user).order_by("match_percentage") 

# Create your views here.
