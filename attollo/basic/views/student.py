from ..models import Student,  User
from ..forms import StudentUpload, StudentUpdate, StudentSignUpForm, NewStudentUpload
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, CreateView, View
from django.views.generic import DetailView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required
from ..decorators import student_required

from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/student')

@method_decorator([login_required, student_required], name='dispatch')
class ProfileView(View):
    template = "student/profileview.html"
    model = Student

    def get_context_data(self, **kwargs):
        kwargs['object'] = Student.objects.get(pk=studpk)
        print(kwargs['object'])
        return super().get_context_data(**kwargs)

    def get(self, request):
        try: # if there is a linked dataid for the user
            studpk = self.request.user.data_id.pk
            print(studpk)
            if Student.objects.filter(pk = studpk).exists():
                student = Student.objects.get(pk=studpk)
                return render(request, self.template, {'object':student})
        except AttributeError as error:
            return redirect('student:upload')

@method_decorator([login_required, student_required], name='dispatch')
class UploadView(CreateView):
    template_name = "student/uploadnewstudent.html"
    model = Student
    form_class = NewStudentUpload
    success_url = '/student/'
    

    def form_valid(self, form):
        student = form.save(commit=False)
        user =  User.objects.get(username=self.request.user.username) 
        student.fname = user.first_name
        student.lname = user.last_name
        student.email = user.username
        student.save()
        user.data_id = student
        user.save()
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch') 
class StudentUpdateView(UpdateView):
    template_name = "student/uploadnewstudent.html"
    model = Student
    form_class = StudentUpdate # Used to skip form validation
    success_url = '/student/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'basestudent.html' # used to display navbar when using update but not upload
        return context
    
    def form_valid(self, form):
        student = form.save(commit=False)
        user =  User.objects.get(username=self.request.user.username) 
        if (student.fname != user.first_name) or (student.lname != user.last_name) or (student.email != user.username):
            user.first_name = student.fname
            user.last_name = student.lname
            if User.objects.filter(username = student.email).exclude(pk = user.pk).exists():
                form.add_error('email', 'User with this email already exists')
                return self.form_invalid(form)
            else:
                user.username = student.email
        student.save()
        user.save()
        return super().form_valid(form)