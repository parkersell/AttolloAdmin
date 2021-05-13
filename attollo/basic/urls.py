from django.urls import path, include
from .views import basic, staff, student


urlpatterns = [
    path('', basic.home, name='home'),
    # all staff views
    # refer to in templates by staff:secondurlname. EX: staff:index
    path('staff/', include(([
        path('', staff.StudentDash.as_view(), name='index'),
        path('allschoolsandstaff/', staff.SchoolandStaffDash.as_view(), name='allschoolsandstaff'),

        path('upload/student/', staff.StudentUploadView.as_view(), name="student_upload"),
        path('upload/school/', staff.SchoolUploadView.as_view(), name="school_upload"),
        path('upload/staff/', staff.StaffUploadView.as_view(), name="staff_upload"),

        path('student/<pk>', staff.StudentDetailView.as_view(), name='student_detail'),
        path('updatestudent/<pk>', staff.StudentUpdateView.as_view(), name='student_update'),
        path('deletestudent/<pk>', staff.StudentDeleteView.as_view(), name="student_delete"),

        path('staffmember/<pk>', staff.StaffDetailView.as_view(), name='staffmember_detail'),
        path('updatestaffmember/<pk>', staff.StaffUpdateView.as_view(), name='staffmember_update'),
        path('deletestaffmember/<pk>', staff.StaffDeleteView.as_view(), name="staffmember_delete"),

        path('school/<pk>', staff.SchoolDetailView.as_view(), name='school_detail'),
        path('updateschool/<pk>', staff.SchoolUpdateView.as_view(), name='school_update'),
        path('deleteschool/<pk>', staff.SchoolDeleteView.as_view(), name="school_delete"),
    ], 'basic'), namespace='staff')),
    # all student views
    path('student/', include(([
        path('', student.ProfileView.as_view(), name='index'),
        path('upload/', student.UploadView.as_view(), name='upload'),
        path('update/<pk>', student.StudentUpdateView.as_view(), name='update'),
    ], 'basic'), namespace='student')),
]

