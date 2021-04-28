from django.core.management.base import BaseCommand
import pandas as pd
from datetime import datetime
from basic.models import Student, School
from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        schools = ["Columbia", "Ephrata", "Lancaster Catholic", "Manhiem Central", "Manhiem Township", "Penn Manor"]
        for i in schools:
            School.objects.get_or_create(name = i)
        cols = ['email','phonenum', 'student_ig','favcandy','address','gender','race','shirt', 'short', 'guard1phonenum', 'guard1email',
        'guard1occ', 'guard1shirt', 'guard2phonenum', 'guard2email', 'guard2occ', 'guard2shirt', 'emergcontact', 'comments', 'schoolid',
        'dob', 'fname', 'lname', 'guard1fname', 'guard1lname', 'guard2fname', 'guard2lname']
        df=pd.read_csv('C:/Users/parke/OneDrive/Documents/GitHub/Attollo/attollo/basic/management/commands/transdf2.csv')


        
        # print(df.head())

        cols =df.columns.tolist()
        for index, r in df.iterrows():
            school = r['schoolid']
            print(school)
            phonenum=r['phonenum']
            guard1phonenum= r['guard1phonenum']
            guard2phonenum= r['guard2phonenum']
            dob =r['dob']
            print(r['phonenum'], r['guard1phonenum'], r['guard2phonenum'])
            if pd.isna(phonenum):
                phonenum =None
            if pd.isna(guard1phonenum):
                guard1phonenum =None
            if pd.isna(guard2phonenum):
                guard2phonenum =None
            if pd.isna(dob):
                dob=None
            else:
                dob= timezone.make_aware(datetime.strptime(dob,  '%Y-%m-%d'))
            schoolid = School.objects.get(name=school)
            Student.objects.get_or_create(email=r['email'], phonenum=phonenum, student_ig=r['student_ig'],favcandy = r['favcandy'],
            address=r['address'], gender=r['gender'], race=r['race'],shirt=r['shirt'],short=r['short'],guard1phonenum= guard1phonenum,
            guard1email=r['guard1email'],guard1occ=r['guard1occ'], guard1shirt=r['guard1shirt'], guard1fname=r['guard1fname'],
            guard1lname = r['guard1lname'],guard2phonenum= guard2phonenum,guard2email=r['guard2email'],
            guard2occ=r['guard2occ'], guard2shirt=r['guard2shirt'], guard2fname=r['guard2fname'],guard2lname = r['guard2lname'],
            emergcontact=r['emergcontact'],comments=r['comments'],
            dob =dob, fname=r['fname'], 
            lname=r['lname'], schoolid = schoolid, gradyear=2003

            )

        self.stdout.write("Created objects")