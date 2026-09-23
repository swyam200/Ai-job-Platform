from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,CandidateProfileSerializer
from .models import CandidateProfile
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[permissions.AllowAny]

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        return Response({
            "message":"you are authenticated!",
            "username":request.user.username,
            "email":request.user.email,
        })

class CandidateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=CandidateProfileSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        profile,created_at=CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile