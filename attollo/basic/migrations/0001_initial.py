# Generated by Django 3.1.7 on 2021-04-05 18:14

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='School Name')),
                ('county', models.CharField(blank=True, max_length=30, verbose_name='County')),
                ('district', models.CharField(blank=True, max_length=30, verbose_name='District')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30, verbose_name='First Name')),
                ('lname', models.CharField(max_length=30, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=30, verbose_name='Email')),
                ('phonenum', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone Number')),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('gradyear', models.IntegerField(verbose_name='Graduation Year')),
                ('gender', models.CharField(max_length=30, verbose_name='Gender')),
                ('image', models.ImageField(blank=True, upload_to='profile_image', verbose_name='Profile')),
                ('comments', models.TextField(blank=True, verbose_name='Additional Comments')),
                ('schoolid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.school', verbose_name='School')),
            ],
        ),
    ]
