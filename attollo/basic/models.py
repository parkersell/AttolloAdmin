from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from datetime import date
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from dateutil.relativedelta import relativedelta
from django.urls import reverse

# https://github.com/daviddrysdale/python-phonenumbers
import phonenumbers


class Student(models.Model):
    fname = models.CharField(max_length=30, verbose_name="First Name")
    lname = models.CharField(max_length=30, verbose_name="Last Name")
    email = models.EmailField(max_length=40, verbose_name="Email")
    phonenum = PhoneNumberField(blank=True, verbose_name="Phone Number")
    dob = models.DateField(verbose_name="Date of Birth")
    # this means that Schools must be defined before students
    schoolid = models.ForeignKey(
        "School", on_delete=models.CASCADE, verbose_name="School")
    # male, female, plus, could make this a choice one
    gradyear = models.IntegerField(blank=True, verbose_name="Graduation Year")
    gender = models.CharField(max_length=30, verbose_name="Gender")
    image = models.ImageField(
        upload_to='profile_image', blank=True, verbose_name="Profile")
    comments = models.TextField(blank=True, verbose_name="Additional Comments")

    def get_fields_forsearch(self):
        allfields = [(field.verbose_name, field.value_from_object(self))
                     for field in self.__class__._meta.fields]
        allfields.insert(4, ("Age", self.age))
        # takes out id
        neededfields = allfields[1:]
        for i in range(len(neededfields)):
            if neededfields[i][0] == "School":
                school_pk = neededfields[i][1]
                neededfields[i] = ("School", School.objects.get(pk=school_pk))
            if neededfields[i][0] == "Phone Number":
                neededfields[i] = ("Phone Number", phonenumbers.format_number(
                    self.phonenum, phonenumbers.PhoneNumberFormat.NATIONAL))
            if neededfields[i][0] == "Year in School":
                neededfields[i] = (
                    "Year in School", self.get_year_in_school_display())
            if neededfields[i][0] == "Date of Birth":
                neededfields[i] = ("Date of Birth", self.dobprint)
            if neededfields[i][0] == "Additional Comments":
                if not (neededfields[i][1]):
                    neededfields[i] = ("Additional Comments", "No Comments")
        return neededfields

    def get_fields_fordetail(self):
        searchfields = self.get_fields_forsearch()
        return searchfields[2:]

    def dobprint(self):
        return self.dob.strftime('%B %d, %Y')

    @ property
    def age(self):
        birthDate = self.dob
        today = date.today()
        age = today.year - birthDate.year - \
            ((today.month, today.day) < (birthDate.month, birthDate.day))
        return age

    def __str__(self):
        return self.fname + ' ' + self.lname

    __repr__ = __str__

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class School(models.Model):
    name = models.CharField(max_length=50, verbose_name="School Name")
    # blank is for form validation, null value is "" for this field
    county = models.CharField(max_length=30, blank=True, verbose_name="County")
    district = models.CharField(
        max_length=30, blank=True, verbose_name="District")

    def __str__(self):
        return self.name

    __repr__ = __str__
