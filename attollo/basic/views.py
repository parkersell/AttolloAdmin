from django.shortcuts import render
from .forms import SchoolUpload, StudentUpload
from .models import Student
from django.views.generic.edit import FormView, CreateView

# Create your views here.
# class StudentUploadView(FormView):
#     template_name = "data_upload.html"
#     form_class = DataUpload
#     success_url = "/upload/student/"

class StudentUploadView(CreateView):
    template_name = "createstudent.html"
    model = Student
    fields = '__all__'
