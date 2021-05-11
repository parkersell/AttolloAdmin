from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from datetime import date
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from dateutil.relativedelta import relativedelta
from django.urls import reverse

# https://pypi.org/project/django-address/
# from address.models import AddressField

# https://pypi.org/project/django-multiselectfield/
# from multiselectfield import MultiSelectField

# https://github.com/daviddrysdale/python-phonenumbers
import phonenumbers

# https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
from django.contrib.auth.models import AbstractUser

#https://github.com/un1t/django-resized
from django_resized import ResizedImageField




class Person(models.Model):
    fname = models.CharField(max_length=30, verbose_name="First Name")
    lname = models.CharField(max_length=30, verbose_name="Last Name")

    def __str__(self):
        return self.fname + ' ' +self.lname

    __repr__ = __str__

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    data_id = models.OneToOneField(Person, on_delete=models.CASCADE, null=True)

def max_value_current_year(value):
    return MaxValueValidator(date.today().year+6)(value)  

class Student(Person):
    SIZE_CHOICES = (
        ('XS','XS')
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    )
    EMERGENCY_CHOICES = (('Guardian 1', 'Guardian 1'),
                         ('Guardian 2', 'Guardian 2'))

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, max_length=50, verbose_name="Email")
    phonenum = PhoneNumberField(null =True, blank=True, verbose_name="Phone Number")
    dob = models.DateField(null = True, verbose_name="Date of Birth")
    # this means that Schools must be defined before students
    schoolid = models.ForeignKey(
        "School", on_delete=models.CASCADE, verbose_name="School")
    # male, female, plus, could make this a choice one
    gradyear = models.IntegerField(verbose_name="Graduation Year", validators=[MinValueValidator(2013), max_value_current_year])
    gender = models.CharField(null = True, max_length=70, verbose_name="Gender")
    image = ResizedImageField(null = True, size=[300, 150], quality = 100,
        upload_to='profile_image', blank=True, verbose_name="Profile Picture")
    race = models.CharField(null = True, max_length=40, verbose_name="Race")
    address = models.CharField(null = True, max_length=60, verbose_name="Address")
    shirt = models.CharField(
        choices=SIZE_CHOICES, verbose_name="Shirt Size", max_length=3)
    short = models.CharField(null = True, 
        choices=SIZE_CHOICES, verbose_name="Short Size", max_length=3)
    student_ig = models.CharField(null = True, 
        max_length=30, verbose_name="Instagram Username", blank=True)
    favcandy = models.CharField(null = True, 
        max_length=30, verbose_name="Favorite Candy", blank=True)
    guard1fname = models.CharField(null = True, 
        max_length=30, verbose_name="Guardian 1 First Name")
    guard1lname = models.CharField(null = True, 
        max_length=30, verbose_name="Guardian 1 Last Name")
    guard1phonenum = PhoneNumberField(null = True, 
        blank=True, verbose_name="Guardian 1 Phone Number")
    guard1email = models.EmailField(null = True, 
        max_length=50, verbose_name="Guardian 1 Email")
    guard1occ = models.CharField(null = True, 
        max_length=60, verbose_name="Guardian 1 Occupation", blank=True)
    guard1shirt = models.CharField(null = True, 
        choices=SIZE_CHOICES, verbose_name="Guardian 1 Shirt Size", max_length=3, blank=True)

    guard2fname = models.CharField(null = True, 
        max_length=30, verbose_name="Guardian 2 First Name", blank=True)
    guard2lname = models.CharField(null = True, 
        max_length=30, verbose_name="Guardian 2 Last Name", blank=True)
    guard2phonenum = PhoneNumberField(null = True, 
        blank=True, verbose_name="Guardian 2 Phone Number")
    guard2email = models.EmailField(null = True, 
        max_length=50, verbose_name="Guardian 2 Email", blank=True)
    guard2occ = models.CharField(null = True, 
        max_length=60, verbose_name="Guardian 2 Occupation", blank=True)
    guard2shirt = models.CharField(null = True, 
        choices=SIZE_CHOICES, verbose_name="Guardian 2 Shirt Size", max_length=3, blank=True)
    emergcontact = models.CharField(null = True, max_length=60, verbose_name="Emergency Contact")
    # comments = models.JSONField(verbose_name="Comments")
    comments = models.TextField(null =True, blank=True, verbose_name="Additional Comments")

    def get_fields_forsearch(self):
        allfields = [(field.verbose_name, field.value_from_object(self))
                     for field in self.__class__._meta.fields]
        allfields.insert(4, ("Has an Account", self.has_user))
        allfields.insert(4, ("Age", self.age))
        # takes out id
        neededfields = allfields[1:]
        # take out person pointer
        del neededfields[2]
        for i in range(len(neededfields)):
            if neededfields[i][0] == "School":
                school_pk = neededfields[i][1]
                neededfields[i] = ("School", School.objects.get(pk=school_pk))
            if "Phone Number" in neededfields[i][0]:
                if neededfields[i][1] != "" and neededfields[i][1] != None:
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
    
    def get_fields_forprofile(self):
        searchfields = self.get_fields_forsearch()
        searchfields = searchfields[2:]
        del searchfields[1]
        return searchfields

    def dobprint(self):
        if self.dob == None:
            return None
        return self.dob.strftime('%B %d, %Y')

    

    @ property
    def age(self):
        birthDate = self.dob
        if birthDate == None:
            return None
        today = date.today()
        age = today.year - birthDate.year - \
            ((today.month, today.day) < (birthDate.month, birthDate.day))
        return age

    @ property
    def has_user(self):
        if User.objects.filter(username = self.email).exists():
            return "Yes"
        else:
            return "No" 

    def get_absolute_url(self):
        return reverse('staff:student_detail', kwargs={'pk': self.pk})


class School(models.Model):
    name = models.CharField(max_length=50, verbose_name="School Name", unique=True)
    # blank is for form validation, null value is "" for this field
    county = models.CharField(max_length=30, blank=True, verbose_name="County")
    district = models.CharField(
        max_length=30, blank=True, verbose_name="District")

    def __str__(self):
        return self.name

    __repr__ = __str__

    def get_absolute_url(self):
        return reverse('staff:school_detail', kwargs={'pk': self.pk})


class Staff(Person):
    email = models.EmailField(max_length=40, verbose_name="Email")

    def get_absolute_url(self):
        return reverse('staff:staffmember_detail', kwargs={'pk': self.pk})