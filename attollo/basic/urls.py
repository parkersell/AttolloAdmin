from django.urls import path

from .views import *

urlpatterns = [
    path('upload/student/', StudentUploadView.as_view(), name="student_upload"),
    path('upload/school/', SchoolUploadView.as_view(), name="school_upload"),
    path('search/', SearchResultsView.as_view(), name="search"),
    path('allstudents', AllStudentsView.as_view(), name ="allstudents"),
    path('', HomePageView.as_view(), name='home'),
]