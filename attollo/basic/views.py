from django.shortcuts import render
from .forms import SchoolUpload, StudentUpload
from .models import Student, School
from .serializers import *
from django.views.generic.edit import FormView, CreateView
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


class StudentUploadView(CreateView):
    template_name = "createstudent.html"
    model = Student
    fields = '__all__'
    success_url = '/'
    form = StudentUpload


class SchoolUploadView(CreateView):
    template_name = "createstudent.html"
    model = School
    fields = '__all__'
    success_url = '/'
    form = SchoolUpload


class HomePageView(TemplateView):
    template_name = 'home.html'


class SearchResultsView(ListView):
    model = Student
    template_name = 'student_results.html'

    queryset = []

    def get_queryset(self):
        query = self.request.GET.get('name')
        object_list = Student.objects.filter(
            Q(fname__icontains=query) | Q(lname__icontains=query)
        )
        return object_list

    # if Book.objects.filter(user=self.user, title=title).exists():
    #         raise forms.ValidationError("You have already written a book with same title.")


class AllStudentsView(ListView):
    model = Student
    template_name = 'student_results.html'


class AllStudentsView(ListView):
    model = Student
    template_name = 'student_results.html'


""" Implementing Django RestFramework"""
