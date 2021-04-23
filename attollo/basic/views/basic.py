from django.shortcuts import render

from basic.models import Student, School, Staff

from django.views.generic.edit import View
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# authorization
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:index')
        else:
            return redirect('student:index')
    return render(request, 'home.html')