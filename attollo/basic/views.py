from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

from .forms import SchoolUpload, StudentUpload
from .models import Student, School
from .serializers import *

from django.views.generic.edit import FormView, CreateView, View
from django.views.generic import TemplateView, ListView
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect


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


"""
Implementing Django RestFramework
 - Creates an api to get the data which allows for better frontend development
 - Will add get, post, update, remove to the available requests
 - Step 5 of link below
    - https://www.digitalocean.com/community/tutorials/how-to-build-a-modern-web-application-to-manage-customer-information-with-django-and-react-on-ubuntu-18-04
"""


# uses a function based view becuase it implements a paginator
@api_view(['GET', 'POST'])
def students_list(request):
    """
 List students, or create a new student.
 """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        students = Student.objects.all()
        page = request.GET.get('page', 1)
        # this is interesting it sets the max number of students per page
        paginator = Paginator(students, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = StudentSerializer(
            data, context={'request': request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data, 'count': paginator.count, 'numpages': paginator.num_pages, 'nextlink': '/api/students/?page=' + str(nextPage), 'prevlink': '/api/students/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


...


@api_view(['GET', 'PUT', 'DELETE'])
def students_detail(request, pk):
    """
    Retrieve, update or delete a student by id/pk.
    """
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(
            student, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(
            student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" 
Testing using startBootstrap

"""


class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        students = Student.objects.all()
        return render(request, self.template, {'students': students})


class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})