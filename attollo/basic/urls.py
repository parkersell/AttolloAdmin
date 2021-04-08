from django.urls import path, include
from .views import *


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('upload/student/', StudentUploadView.as_view(), name="student_upload"),
    path('upload/school/', SchoolUploadView.as_view(), name="school_upload"),
    # restframeworkurls
    path('api/students/', students_list),
    path('api/students/<pk>', students_detail),
    # start bootstrap
    path('', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),

    path('student/<pk>', StudentDetailView.as_view(), name='student_detail'),
    path('updatestudent/<pk>', StudentUpdateView.as_view(), name='student_update'),
    path('deletestudent/<pk>', StudentDeleteView.as_view(), name="student_delete"),

]
