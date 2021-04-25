from ..models import Student, School, Staff, User
from ..forms import SchoolUpload, StudentUpload, StudentUpdate, StaffSignUpForm, StaffUpload
from django.views.generic.edit import FormView, CreateView, View
from django.views.generic import DetailView, DeleteView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth import login, authenticate

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import staff_required

class StaffSignUpView(CreateView):
    model = User
    form_class = StaffSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/staff')

@method_decorator([login_required, staff_required], name='dispatch')
class StudentDash(View):
    template = 'staff-studentdash.html'

    def get(self, request):
        students = Student.objects.all()
        return render(request, self.template, {'students': students})

@method_decorator([login_required, staff_required], name='dispatch')
class SchoolandStaffDash(View):
    template = 'staff-schooldash.html'

    def get(self, request):
        staff = Staff.objects.all()
        schools = School.objects.all()
        return render(request, self.template, {'staff': staff, 'schools':schools})

"""
Student Object Views
"""

@method_decorator([login_required, staff_required], name='dispatch')
class StudentUploadView(CreateView):
    template_name = "staff-uploadobject.html"
    model = Student
    form_class = StudentUpload

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "Student"
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class StudentDetailView(DetailView):
    model = Student
    template_name = "staff-studentdetail.html"


@method_decorator([login_required, staff_required], name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    success_url = '/staff'


@method_decorator([login_required, staff_required], name='dispatch')
class StudentUpdateView(UpdateView):
    template_name = "staff-uploadobject.html"
    model = Student
    form_class = StudentUpdate # Used to skip form validation

    def form_valid(self, form):
        student = form.save(commit=False)
        try:
            user =  User.objects.get(data_id=student) 
            if (student.fname != user.first_name) or (student.lname != user.last_name) or (student.email != user.username):
                user.first_name = student.fname
                user.last_name = student.lname
                if User.objects.filter(username = student.email).exclude(pk =user.pk).exists():
                    form.add_error('email', 'User with this email already exists')
                    return self.form_invalid(form)
                else:
                    user.username = student.email
            user.save()
        except User.DoesNotExist:
            pass
        student.save()
        return super().form_valid(form)

"""
School Object Views
"""

@method_decorator([login_required, staff_required], name='dispatch')
class SchoolUploadView(CreateView):
    template_name = "staff-uploadobject.html"
    model = School
    form_class = SchoolUpload
    success_url = '/staff/allschoolsandstaff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "School"
        return context


@method_decorator([login_required, staff_required], name='dispatch')
class SchoolDetailView(DetailView):
    model = School
    template_name = "staff-schooldetail.html"


@method_decorator([login_required, staff_required], name='dispatch')
class SchoolDeleteView(DeleteView):
    model = School
    success_url = '/staff/allschoolsandstaff'


@method_decorator([login_required, staff_required], name='dispatch')
class SchoolUpdateView(UpdateView):
    template_name = "staff-uploadobject.html"
    model = School
    fields = '__all__'

"""
Staff Object Views
"""

@method_decorator([login_required, staff_required], name='dispatch')
class StaffUploadView(CreateView):
    template_name = "staff-uploadobject.html"
    model = Staff
    form_class = StaffUpload
    success_url = '/staff/allschoolsandstaff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = "Staff"
        return context

@method_decorator([login_required, staff_required], name='dispatch')
class StaffDetailView(DetailView):
    model = Staff
    template_name = "staff-staffdetail.html"


@method_decorator([login_required, staff_required], name='dispatch')
class StaffDeleteView(DeleteView):
    model = Staff
    success_url = '/staff/allschoolsandstaff'


@method_decorator([login_required, staff_required], name='dispatch')
class StaffUpdateView(UpdateView):
    template_name = "staff-uploadobject.html"
    model = Staff
    fields = '__all__'
