from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    path('upload/student/', StudentUploadView.as_view(), name="student_upload"),
    path('upload/school/', SchoolUploadView.as_view(), name="school_upload"),
    path('search/', SearchResultsView.as_view(), name="search"),
    path('allstudents/', AllStudentsView.as_view(), name="allstudents"),
    path('home/', HomePageView.as_view(), name='home'),
    # restframeworkurls
    url(r'^api/students/$', students_list),
    url(r'^api/students/(?P<pk>[0-9]+)$', students_detail),
    # start bootstrap
    path('', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
]
