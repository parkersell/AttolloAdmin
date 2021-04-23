from django.test import TestCase
from basic.models import Student, School
from datetime import datetime
from django.utils import timezone

from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from basic.views import *
from basic.urls import urlpatterns as basic_urlpatterns # import urlpatterns of the app
"""
For models need to test 
 - custom functions
 - if contsraints are proper, aka length <30, if that feature works
 - 
From https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
"""

# class StudentTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         School.objects.create(name="Central Dauphin High School", county ='', district='')
#         Student.objects.create(fname = "Bob", lname = "Jones", email = "bobjones@gmail.com", phonenum = 7171234567, 
#                                 age = 16, dob = timezone.make_aware(datetime(2004, 3,26)), #makes a datetime aware
#                                 schoolid =  School.objects.get(pk=1), schoolyear = 10, gender = "male")
        

#     def test_student_fname_label(self):
#         student = Student.objects.get(id=1)
#         field_label = student._meta.get_field('fname').verbose_name
#         self.assertEqual(field_label, 'First Name')
    
    
#     def test_student_lname_label(self):
#         student = Student.objects.get(id=1)
#         field_label = student._meta.get_field('lname').verbose_name
#         self.assertEqual(field_label, 'Last Name')
    
    
#     def test_student_email_label(self):
#         student = Student.objects.get(id=1)
#         field_label = student._meta.get_field('email').verbose_name
#         self.assertEqual(field_label, 'Email')


""" For Testing login required mixin
From here https://stackoverflow.com/questions/62239228/writing-unit-test-for-my-class-based-views-which-also-require-loginrequiredmixin
"""


class TestTeamsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        School.objects.create(name="Central Dauphin High School", county ='', district='')
        Student.objects.create(fname = "Bob", lname = "Jones", email = "bobjones@gmail.com", phonenum = '+17171234567', 
                                 dob = timezone.make_aware(datetime(2004, 3,26)), #makes a datetime aware
                                schoolid =  School.objects.get(pk=1), gender = "male", race = Student.RACE_CHOICES[0], 
                                shirt = Student.SIZE_CHOICES[0],  short = Student.SIZE_CHOICES[0], 
                                gradyear = 1002)
        
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test1',
            email='abc1@gmail.com',
            first_name='t',
            last_name='u',
            password='password'
        )
        self.views = [Index, SchoolUploadView, StudentUploadView, StudentDetailView, StudentDeleteView, StudentUpdateView]
        self.urls = ["/",'upload/school/' , 'upload/student/', 'student/1', 'deletestudent/1', 'updatestudent/1']


    
    def test0_with_anonymous_user(self):
        i = 0
        request = self.factory.get(self.urls[i])
        request.user = AnonymousUser()
        if i >2:
            response = self.views[i].as_view()(request, pk =1)
        else:
            response = self.views[i].as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test1_with_anonymous_user(self):
        i = 1
        request = self.factory.get(self.urls[i])
        request.user = AnonymousUser()
        if i >2:
            response = self.views[i].as_view()(request, pk =1)
        else:
            response = self.views[i].as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test2_with_anonymous_user(self):
        i = 2
        request = self.factory.get(self.urls[i])
        request.user = AnonymousUser()
        if i >2:
            response = self.views[i].as_view()(request, pk =1)
        else:
            response = self.views[i].as_view()(request)
        self.assertEqual(response.status_code, 302)
    
    def test3_with_anonymous_user(self):
        i = 3
        request = self.factory.get(self.urls[i])
        request.user = AnonymousUser()
        if i >2:
            response = self.views[i].as_view()(request, pk =1)
        else:
            response = self.views[i].as_view()(request)
        self.assertEqual(response.status_code, 302)
    
    def test4_with_anonymous_user(self):
        i = 4
        request = self.factory.get(self.urls[i])
        request.user = AnonymousUser()
        if i >2:
            response = self.views[i].as_view()(request, pk =1)
        else:
            response = self.views[i].as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test5_with_anonymous_user(self):
        i = 5
        request = self.factory.get(self.urls[i])
        request.user = AnonymousUser()
        if i >2:
            response = self.views[i].as_view()(request, pk =1)
        else:
            response = self.views[i].as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_with_valid_user(self):
        for i in range(len(self.views)):
            request = self.factory.get(self.urls[i])
            request.user = self.user
            if i >2:
                response = self.views[i].as_view()(request, pk =1)
            else:
                response = self.views[i].as_view()(request)
            self.assertEqual(response.status_code, 200)