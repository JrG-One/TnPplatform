# Generated by Django 5.0.2 on 2024-03-09 08:28

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Job_Opening', '0001_initial'),
        ('TrainingProgram', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('personal_email', models.EmailField(blank=True, max_length=254, verbose_name='personal email address')),
                ('whatsapp_number', models.CharField(blank=True, max_length=15)),
                ('address', models.TextField(blank=True)),
                ('Student_ID', models.CharField(default='studentID', max_length=20, unique=True)),
                ('Branch', models.CharField(choices=[('CSE', 'CSE'), ('ECE', 'ECE')], max_length=50)),
                ('Resume_Link', models.CharField(default='blank', max_length=300)),
                ('CGPA', models.DecimalField(decimal_places=2, default='5.00', max_digits=3)),
                ('Block_All_Applications', models.BooleanField(default=False)),
                ('Access_Token', models.CharField(max_length=300, null=True)),
                ('resume_json', models.JSONField(blank=True, null=True)),
                ('Placed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Job_Opening.job_opening')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Job_Student_Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Blocked', models.BooleanField()),
                ('Status', models.CharField(max_length=1)),
                ('Job_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Job_Opening.job_opening')),
                ('Student_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Training_Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Attended', models.BooleanField()),
                ('Student_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Training_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrainingProgram.trainingprogram')),
            ],
        ),
    ]
