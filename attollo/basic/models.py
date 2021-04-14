from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from datetime import date
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from dateutil.relativedelta import relativedelta
from django.urls import reverse

# https://pypi.org/project/django-address/
from address.models import AddressField

# https://pypi.org/project/django-multiselectfield/
from multiselectfield import MultiSelectField

# https://github.com/daviddrysdale/python-phonenumbers
import phonenumbers


class Student(models.Model):
    RACE_CHOICES = ((1, 'Caucasian'),
                    (2, 'Hispanic'),
                    (3, 'African American'),
                    (4, 'Asian'),
                    (5, 'American Indian'),
                    (6, 'Pacific Islander'))
    SIZE_CHOICES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    )
    EMERGENCY_CHOICES = (('Guardian 1', 'Guardian 1'),
                         ('Guardian 2', 'Guardian 2'))
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
    race = MultiSelectField(choices=RACE_CHOICES,
                            max_choices=3, verbose_name="Race")
    # address = AddressField(verbose_name="Address")
    shirt = models.CharField(
        choices=SIZE_CHOICES, verbose_name="Shirt size", max_length=3)
    short = models.CharField(
        choices=SIZE_CHOICES, verbose_name="Short size", max_length=3)
    student_ig = models.CharField(
        max_length=30, verbose_name="Instagram Username", blank=True)
    favcandy = models.CharField(
        max_length=30, verbose_name="Favorite Candy", blank=True)
    guard1fname = models.CharField(
        max_length=30, verbose_name="Guardian 1 First Name")
    guard1sname = models.CharField(
        max_length=30, verbose_name="Guardian 1 Second Name")
    guard1phonenum = PhoneNumberField(
        blank=True, verbose_name="Guardian 1 Phone Number")
    guard1email = models.EmailField(
        max_length=40, verbose_name="Guardian 1 Email")
    gaurd1occ = models.CharField(
        max_length=40, verbose_name="Guardian 1 Occupation", blank=True)
    guard1shirt = models.CharField(
        choices=SIZE_CHOICES, verbose_name="Guardian 1 Shirt size", max_length=3, blank=True)

    guard2fname = models.CharField(
        max_length=30, verbose_name="Guardian 2 First Name", blank=True)
    guard2sname = models.CharField(
        max_length=30, verbose_name="Guardian 2 Second Name", blank=True)
    guard2phonenum = PhoneNumberField(
        blank=True, verbose_name="Guardian 2 Phone Number")
    guard2email = models.EmailField(
        max_length=40, verbose_name="Guardian 2 Email", blank=True)
    gaurd2occ = models.CharField(
        max_length=40, verbose_name="Guardian 2 Occupation", blank=True)
    guard2shirt = models.CharField(
        choices=SIZE_CHOICES, verbose_name="Guardian 2 Shirt size", max_length=3, blank=True)
    emergcontact = models.CharField(
        choices=EMERGENCY_CHOICES, max_length=20, verbose_name="Emergency Contact")
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
            if "Phone Number" in neededfields[i][0]:
                neededfields[i] = (neededfields[i][0], phonenumbers.format_number(
                    neededfields[i][1], phonenumbers.PhoneNumberFormat.NATIONAL))
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
