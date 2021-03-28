from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Person(models.Model):
    fname = models.CharField(max_length=30, verbose_name="First Name")
    lname = models.CharField(max_length=30, verbose_name="Last Name")
    email = models.CharField(max_length=30, verbose_name="Email")

    def __str__(self):
        return self.fname + ' ' +self.lname

    __repr__ = __str__

class Student(Person):
    phonenum = models.IntegerField(blank = True, verbose_name="Phone Number")
    age = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Age")
    dob = models.DateTimeField(verbose_name="Date of Birth")
    schoolid = models.ForeignKey("School", on_delete=models.CASCADE, verbose_name="School") # this means that Schools must be defined before students
    schoolyear = models.IntegerField(verbose_name="Year in School") # 9, 10, 11, 12
    gender = models.CharField(max_length=30, verbose_name="Gender") # male, female, plus, could make this a choice one
    image = models.ImageField(upload_to='profile_image', blank=True, verbose_name="Image")
    comments = models.TextField(blank=True, verbose_name="Additional Comments")

    
class School(models.Model):
    name = models.CharField(max_length=50, verbose_name="School Name")
    county = models.CharField(max_length=30, blank =True, verbose_name="County") # blank is for form validation, null value is "" for this field
    district = models.CharField(max_length=30, blank =True, verbose_name="District")

    def __str__(self):
        return self.name
    
    __repr__ = __str__

class Employee(Person):
    position = models.CharField(max_length=30) # just a variable I found online, honestly don't think we need it
