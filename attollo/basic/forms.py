from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, School, Staff, User
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db import transaction
# https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from datetime import date

import json
from django.forms import widgets

def year_choices():
    return [(r,r) for r in range(2013, date.today().year+6)]

# for comments
class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            print("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)


# Used for update
class StudentUpdate(forms.ModelForm):
    gradyear = forms.TypedChoiceField(coerce=int, choices=year_choices)
    class Meta:
        model = Student
        fields = '__all__'
        field_classes = {
            'phonenum': PhoneNumberField,
            
        }
        widgets = {
            'phonenum': PhoneNumberInternationalFallbackWidget(),
            # 'comments': PrettyJSONWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        ## if you modify this make sure its modified in the other one. 
        self.helper.layout = Layout(
            HTML('<h1 class="h4 mb-2 text-gray-800">Student Personal Info</h1>'),
            HTML('<hr></hr>'),
            HTML('<div class="text"><p>All things with an * are required </a></div>'),
            Row(
                Column('fname', css_class='form-group col-md-6 mb-0'),
                Column('lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('phonenum', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('schoolid', css_class='form-group col-md-6 mb-0'),
                Column('gradyear', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('dob', css_class='form-group col-md-6 mb-0'),
            ), 
            Row(
                Column('gender', css_class='form-group col-md-6 mb-0'),
            ), 
            'image',
            'race',
            Row(
                Column('shirt', css_class='form-group col-md-6 mb-0'),
                Column('short', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('student_ig', css_class='form-group col-md-6 mb-0'),
            ), 
            'favcandy',
            HTML('<h1 class="h4 mb-2 text-gray-800">Guardian 1 Info</h1>'),
            HTML('<hr></hr>'),
            Row(
                Column('guard1fname', css_class='form-group col-md-6 mb-0'),
                Column('guard1lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('guard1email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('guard1phonenum', css_class='form-group col-md-6 mb-0'),
            ),
            'guard1occ',
            Row(
                Column('guard1shirt', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h1 class="h4 mb-2 text-gray-800">Guardian 2 Info</h1>'),
            HTML('<hr></hr>'),
            Row(
                Column('guard2fname', css_class='form-group col-md-6 mb-0'),
                Column('guard2lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('guard2email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('guard2phonenum', css_class='form-group col-md-6 mb-0'),
            ),
            'guard2occ',
            Row(
                Column('guard2shirt', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<hr></hr>'),
            HTML('<div class="text"><p>Choose which guardian should be the primary contact in case of an emergency </a></div>'),
            Row(
                Column('emergcontact', css_class='form-group col-md-6 mb-0'),
            ),
            'comments',
            Submit('submit', 'Upload')
        )
    

#used for upload
class StudentUpload(StudentUpdate):

    def clean(self):
        data = super().clean()

        if Student.objects.filter(fname=data.get("fname"), lname=self.data.get("lname"), email=data.get("email")).exists():
            s = Student.objects.filter(fname=data.get(
                "fname"), lname=self.data.get("lname"), email=data.get("email"))
            print(s)
            raise forms.ValidationError(mark_safe(
                'You have already created a student with same name and email. '
                'Would you like to update? If so, click this <a href="{0}">Update User</a> link'.format(reverse('staff:student_update', kwargs={'pk': s[0].pk})))
            )


class NewStudentUpload(StudentUpdate):
    class Meta:
        model = Student
        exclude = ['fname', 'lname', 'email']

    ## if you modify this make sure its modified in the other one.
    def __init__(self, *args, **kwargs):
        super(NewStudentUpload, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h1 class="h4 mb-2 text-gray-800">Student Personal Info</h1>'),
            HTML('<hr></hr>'),
            HTML('<div class="text"><p>All things with an * are required </a></div>'),
            Row(
                Column('schoolid', css_class='form-group col-md-6 mb-0'),
                Column('gradyear', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phonenum', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('dob', css_class='form-group col-md-6 mb-0'),
            ), 
            Row(
                Column('gender', css_class='form-group col-md-6 mb-0'),
            ), 
            'image',
            'race',
            Row(
                Column('shirt', css_class='form-group col-md-6 mb-0'),
                Column('short', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('student_ig', css_class='form-group col-md-6 mb-0'),
            ), 
            'favcandy',
            HTML('<h1 class="h4 mb-2 text-gray-800">Guardian 1 Info</h1>'),
            HTML('<hr></hr>'),
            Row(
                Column('guard1fname', css_class='form-group col-md-6 mb-0'),
                Column('guard1lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('guard1email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('guard1phonenum', css_class='form-group col-md-6 mb-0'),
            ),
            'guard1occ',
            Row(
                Column('guard1shirt', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<h1 class="h4 mb-2 text-gray-800">Guardian 2 Info</h1>'),
            HTML('<hr></hr>'),
            Row(
                Column('guard2fname', css_class='form-group col-md-6 mb-0'),
                Column('guard2lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('guard2email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('guard2phonenum', css_class='form-group col-md-6 mb-0'),
            ),
            'guard2occ',
            Row(
                Column('guard2shirt', css_class='form-group col-md-6 mb-0'),
            ),
            HTML('<hr></hr>'),
            HTML('<div class="text"><p>Choose which guardian should be the primary contact in case of an emergency </a></div>'),
            Row(
                Column('emergcontact', css_class='form-group col-md-6 mb-0'),
            ),
            'comments',
            Submit('submit', 'Upload')
        )

    

# This is used to create a staff object
class StaffUpload(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

    def clean(self):
        data = super().clean()

        if Staff.objects.filter(fname=data.get("fname"), lname=self.data.get("lname"), email=data.get("email")).exists():
            s = Staff.objects.filter(fname=data.get(
                "fname"), lname=self.data.get("lname"), email=data.get("email"))
            raise forms.ValidationError(mark_safe(
                'You have already created a staff member with same name and email. '
                'Would you like to update? If so, click this <a href="{0}">Update Staff Member</a> link'.format(reverse('staff:staffmember_update', kwargs={'pk': s[0].pk})))
            )



class SchoolUpload(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'

    def clean(self):
        data = super().clean()

        if School.objects.filter(name=self.data.get("name")).exists():
            s = School.objects.filter(name=self.data.get("name"))
            raise forms.ValidationError(mark_safe(
                'You have already created a School with same name. '
                'Would you like to update? If so, click this <a href="{0}">Update School</a> link'.format(reverse('staff:school_update', kwargs={'pk': s[0].pk})))
            )

    

#This is used to create a staff user
class StaffSignUpForm(UserCreationForm):
    
    fname = forms.CharField(max_length=30, label='First name')
    lname = forms.CharField(max_length=30, label='Last name')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('fname', 'lname',)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.data_id =Staff.objects.get(fname=self.cleaned_data['fname'], lname=self.cleaned_data['lname'], email=self.cleaned_data['username'])
        print(user.data_id)
        if commit:
            user.save()
        return user

    def clean(self):
        data = super().clean()

        if not (Staff.objects.filter(fname=data.get("fname"), lname=self.data.get("lname"), email=data.get("username")).exists()):
            
            raise forms.ValidationError(mark_safe(
                'You are not authorized to become a staff member.  '
                'Did you mean to be a student? If so, click this <a href="{0}">Student Signup </a> link'.format(reverse('home')) #TODO change to student signin
            ))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('fname', css_class='form-group col-md-6 mb-0'),
                Column('lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'password1',
            'password2',
            Submit('submit', 'Sign in')
        )
    
class StudentSignUpForm(UserCreationForm):
    fname = forms.CharField(max_length=30, label='First name')
    lname = forms.CharField(max_length=30, label='Last name')
    username = forms.RegexField(label=("Email"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': ("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('fname', 'lname',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        if Student.objects.filter(fname=self.cleaned_data['fname'], lname=self.cleaned_data['lname'], email=self.cleaned_data['username']).exists():
            user.data_id =Student.objects.get(fname=self.cleaned_data['fname'], lname=self.cleaned_data['lname'], email=self.cleaned_data['username'])
        else:
            user.first_name = self.cleaned_data['fname']
            user.last_name = self.cleaned_data['lname']
        user.save()
        return user

    # def clean(self):
    #     data = super().clean()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('fname', css_class='form-group col-md-6 mb-0'),
                Column('lname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'password1',
            'password2',
            Submit('submit', 'Sign in'),
        )
