from django.urls import path
from .views import RegisterView,ProfileView,CandidateProfileView
urlpatterns=[
    path("register/",RegisterView.as_view(),name="register"),
    path("profile/",CandidateProfileView.as_view(),name="profile"),
    
]