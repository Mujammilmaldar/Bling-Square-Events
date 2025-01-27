# Generated by Django 4.2.5 on 2024-03-18 07:01

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('category', models.CharField(choices=[('employee', 'Employee'), ('admin', 'Admin'), ('hr', 'HR'), ('manager', 'Manager'), ('intern', 'Intern')], default='employee', max_length=20)),
                ('photo', models.ImageField(upload_to='photos/')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('dob', models.DateField(default=datetime.date.today)),
                ('joiningdate', models.DateField(default=datetime.date.today)),
                ('address', models.TextField()),
                ('designation', models.CharField(max_length=100)),
                ('mobileno', models.CharField(max_length=11, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
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
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.BigIntegerField(unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bookings_count', models.PositiveIntegerField(default=0)),
                ('leadperson', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeExcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.FileField(upload_to='employee_excel')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('type_of_event', models.TextField(max_length=200)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20)),
                ('mode_of_payment', models.CharField(choices=[('cash', 'Cash'), ('online', 'Online'), ('not_yet', 'Not Yet')], default='not_yet', max_length=20)),
                ('payment_status', models.CharField(choices=[('unpaid', 'Unpaid'), ('half paid', 'Half Paid'), ('paid', 'Paid')], default='not_yet', max_length=20)),
                ('payment', models.CharField(default=0, max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.client')),
            ],
        ),
        migrations.CreateModel(
            name='EventExcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.FileField(upload_to='event_excel')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=200)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('leave_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_completion_percentage', models.PositiveIntegerField(default=0)),
                ('language', models.CharField(choices=[('en', 'English'), ('hi', 'Hindi')], default='en-us', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.client')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemOfEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], max_length=10)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='dashboard.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_event', models.TextField()),
                ('event_date', models.DateField()),
                ('event_start_at', models.DateField()),
                ('event_end_at', models.DateField()),
                ('day_of_event', models.TextField()),
                ('list_of_good', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.event')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_goods', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_goods', to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.venue')),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendors_name', models.CharField(max_length=100)),
                ('vendors_organisation_name', models.CharField(max_length=100)),
                ('particulars', models.CharField(max_length=200)),
                ('details', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('paid', 'Paid'), ('not_paid', 'Not Paid'), ('half_paid', 'Half Paid')], default='not_paid', max_length=20)),
                ('mode_of_payment', models.CharField(choices=[('cash', 'Cash'), ('online', 'Online'), ('not_yet', 'Not Yet')], default='not_yet', max_length=20)),
                ('payment_made_by', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='expenses')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.venue'),
        ),
        migrations.CreateModel(
            name='DocumentOfEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adharcard', models.FileField(upload_to='document/')),
                ('pancard', models.FileField(upload_to='document/')),
                ('voterid', models.FileField(upload_to='document/')),
                ('license', models.FileField(upload_to='document/')),
                ('passport', models.FileField(upload_to='document/')),
                ('eid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('shift', models.CharField(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')], max_length=10)),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
