from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

commonlayout1 = Layout(
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
        )

nameemaillayout = Layout(
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
        )

addresslayout = Layout(
            'address_1',
            'address_2',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
)
commonlayout2 = Layout(
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
            Submit('submit', 'Upload'),
)

newstudentuploadlayout = Layout(
            HTML('<h1 class="h4 mb-2 text-gray-800">Student Personal Info</h1>'),
            HTML('<hr></hr>'),
            HTML('<div class="text"><p>All things with an * are required </a></div>'),
            commonlayout1,
            addresslayout,
            commonlayout2,
        )

uploadlayout = Layout(
            nameemaillayout, 
            commonlayout1, 
            addresslayout, 
            commonlayout2
)

updatelayout = Layout(
            nameemaillayout,
            commonlayout1,
            'address',
            commonlayout2,
    )