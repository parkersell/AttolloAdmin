from django.core.management.base import BaseCommand
import pandas as pd
from datetime import datetime
from basic.models import Student, School
from django.utils import timezone
from attollo.settings.common import COMMAND_FOLDER
import os

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

        parser.add_argument('gradyear', nargs='+', type=int)

    def handle(self, *args, **options):
        print(options['filename'][0], options['gradyear'][0])
        schools = ["Columbia", "Ephrata", "Lancaster Catholic", "Manheim Central", "Manheim Township", "Penn Manor"]
        for i in schools:
            School.objects.get_or_create(name = i)
        cols = ['email','phonenum', 'student_ig','favcandy','address','gender','race','shirt', 'short', 'guard1phonenum', 'guard1email',
        'guard1occ', 'guard1shirt', 'guard2phonenum', 'guard2email', 'guard2occ', 'guard2shirt', 'emergcontact', 'comments', 'schoolid',
        'dob', 'fname', 'lname', 'guard1fname', 'guard1lname', 'guard2fname', 'guard2lname']
        df=pd.read_csv(os.path.join(COMMAND_FOLDER, options['filename'][0]))


        
        # print(df.head())
        count = 0
        cols =df.columns.tolist()
        for index, r in df.iterrows():
            school = r['schoolid']
            phonenum=r['phonenum']
            guard1phonenum= r['guard1phonenum']
            guard2phonenum= r['guard2phonenum']
            dob =r['dob']
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
            studobj, boolean = Student.objects.get_or_create(email=r['email'], phonenum=phonenum, student_ig=r['student_ig'],favcandy = r['favcandy'],
            address=r['address'], gender=r['gender'], race=r['race'],shirt=r['shirt'],short=r['short'],guard1phonenum= guard1phonenum,
            guard1email=r['guard1email'],guard1occ=r['guard1occ'], guard1shirt=r['guard1shirt'], guard1fname=r['guard1fname'],
            guard1lname = r['guard1lname'],guard2phonenum= guard2phonenum,guard2email=r['guard2email'],
            guard2occ=r['guard2occ'], guard2shirt=r['guard2shirt'], guard2fname=r['guard2fname'],guard2lname = r['guard2lname'],
            emergcontact=r['emergcontact'],comments=r['comments'],
            dob =dob, fname=r['fname'], 
            lname=r['lname'], schoolid = schoolid, gradyear=options['gradyear'][0]
            )
            if boolean:
                self.stdout.write(studobj.fname)
                count+=1
            

        self.stdout.write("Created " + str(count) +" objects")