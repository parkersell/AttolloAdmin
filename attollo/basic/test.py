from django.test import TestCase
from basic.models import Student, School, Person, Employee
from datetime import datetime
from django.utils import timezone

"""
For models need to test 
 - custom functions
 - if contsraints are proper, aka length <30, if that feature works
 - 
From https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
"""

class StudentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        School.objects.create(name="Central Dauphin High School", county ='', district='')
        Student.objects.create(fname = "Bob", lname = "Jones", email = "bobjones@gmail.com", phonenum = 7171234567, 
                                age = 16, dob = timezone.make_aware(datetime(2004, 3,26)), #makes a datetime aware
                                schoolid =  School.objects.get(pk=1), schoolyear = 10, gender = "male")
        

    def test_student_fname_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('fname').verbose_name
        self.assertEqual(field_label, 'First Name')
    
    
    def test_student_lname_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('lname').verbose_name
        self.assertEqual(field_label, 'Last Name')
    
    
    def test_student_email_label(self):
        student = Student.objects.get(id=1)
        field_label = student._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Email')