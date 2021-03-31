from rest_framework import serializers
from .models import School, Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('pk', 'fname', 'lname', 'email', 'phonenum', 'age', 'dob',
                  'schoolid', 'year_in_school', 'gender', 'image', 'comments')


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'
