from django import forms
from .models import Student, School
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.urls import reverse

# this isnt used


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        field_classes = {
            'phonenum': PhoneNumberField,
        }
        widgets = {
            'phonenum': PhoneNumberInternationalFallbackWidget(attrs={'class': "form-control bg-light", "style": "width: 200px;"})
        }


class StudentUpload(StudentForm):

    def clean(self):
        data = super().clean()

        if Student.objects.filter(fname=data.get("fname"), lname=self.data.get("lname"), dob=data.get("dob")).exists():
            s = Student.objects.filter(fname=data.get(
                "fname"), lname=self.data.get("lname"), dob=data.get("dob"))
            print(s)
            raise forms.ValidationError(mark_safe(
                'You have already created a student with same name and birthdate. '
                'Would you like to update? If so, click this <a href="{0}">Update User</a> link'.format(reverse('student_update', kwargs={'pk': s[0].pk})))
            )


class SchoolUpload(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
