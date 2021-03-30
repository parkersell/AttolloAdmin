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

    # def get_absolute_url(self):
    #     return reverse('books:detail', args=[self.id])
    

class Student(Person):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    phonenum = models.IntegerField(blank = True, verbose_name="Phone Number")
    age = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Age")
    dob = models.DateTimeField(verbose_name="Date of Birth")
    schoolid = models.ForeignKey("School", on_delete=models.CASCADE, verbose_name="School") # this means that Schools must be defined before students
    year_in_school = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default=FRESHMAN, verbose_name="Year in school") 
    gender = models.CharField(max_length=30, verbose_name="Gender") # male, female, plus, could make this a choice one
    image = models.ImageField(upload_to='profile_image', blank=True, verbose_name="Profile")
    comments = models.TextField(blank=True, verbose_name="Additional Comments")

    def get_fields_forsearch(self):
        allfields = [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]
        neededfields = allfields[3:4] +allfields[5:]# takes out id and name and person pointer
        for i in range(len(neededfields)):
            if neededfields[i][0] == "School":
                school_pk = neededfields[i][1]
                neededfields[i] = ("School", School.objects.get(pk=school_pk))
        neededfields = neededfields
        return neededfields
    

    
class School(models.Model):
    name = models.CharField(max_length=50, verbose_name="School Name")
    county = models.CharField(max_length=30, blank =True, verbose_name="County") # blank is for form validation, null value is "" for this field
    district = models.CharField(max_length=30, blank =True, verbose_name="District")

    def __str__(self):
        return self.name
    
    __repr__ = __str__

    

class Employee(Person):
    position = models.CharField(max_length=30) # just a variable I found online, honestly don't think we need it
