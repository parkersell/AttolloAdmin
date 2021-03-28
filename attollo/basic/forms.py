from django import forms
from .models import Student, School

class StudentUpload(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    
class SchoolUpload(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'