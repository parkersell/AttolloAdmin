from ..models import Student,  User
from ..forms import StudentUpload, StudentUpdate, StudentSignUpForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, CreateView, View
from django.views.generic import DetailView, DeleteView, UpdateView

from django.shortcuts import get_object_or_404

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

class ProfileView(View):
    template = "profileview.html"
    model = Student

    def get_context_data(self, **kwargs):
        kwargs['object'] = Student.objects.get(pk=studpk)
        return super().get_context_data(**kwargs)

    def get(self, request):
        studpk = self.request.user.pk
        print(studpk)
        if Student.objects.filter(pk = studpk).exists():
            student = Student.objects.get(pk=studpk)
            return render(request, self.template, {'object':student})
        else:
            return redirect('student:upload')

class UploadView(CreateView):
    template_name = "uploadnewstudent.html"
    model = Student
    form_class = StudentUpdate
    success_url = '/student'
    
class StudentUpdateView(UpdateView):
    template_name = "uploadnewstudent.html"
    model = Student
    form_class = StudentUpdate # Used to skip form validation
    success_url = '/student'