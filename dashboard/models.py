from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    USER_ROLES = (
        ('employee', 'Employee'),
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('manager', 'Manager'),
        ('intern', 'Intern'),
    )

    category = models.CharField(max_length=20, choices=USER_ROLES, default='employee')
    photo = models.ImageField(upload_to='photos/')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    dob = models.DateField(default=datetime.date.today)
    joiningdate = models.DateField(default=datetime.date.today)
    address = models.TextField()
    designation = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=11, unique=True)
    active = models.BooleanField(default=True)  # Track active status
    last_activity = models.DateTimeField(auto_now=True)  # Track last activity timestamp
    
    def total_working_duration(self):
        """Calculate total working duration for the employee."""
        work_logs = WorkLog.objects.filter(employee=self)
        total_duration = sum((log.end_time - log.start_time).total_seconds() for log in work_logs)
        return datetime.timedelta(seconds=total_duration)
    
    
from django.contrib.auth import get_user_model
User = get_user_model()
class UserLanguage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)

class WorkLog(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    leave_reason = models.CharField(max_length=100, blank=True, null=True)

    def duration(self):
        """Calculate the duration of the work log."""
        return self.end_time - self.start_time

class Internship(models.Model):
    intern = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def is_within_internship_period(self):
        """Check if the intern is within the allowed internship period."""
        if not self.end_date:
            return True
        internship_duration = self.end_date - self.start_date
        return internship_duration.days <= 180  # 180 days is approximately 6 months



class Client(models.Model):
    name = models.CharField(max_length=100)
    number = models.BigIntegerField(unique = True)
    email = models.EmailField(unique=True)
    bookings_count = models.PositiveIntegerField(default=0)  # Track number of bookings
    leadperson = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online'),
        ('not_yet_decided', 'Not Yet Decided'),
    )
    
    TYPE_OF_EVENT_CHOICES = (
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('meeting', 'Meeting'),
        ('party', 'Party'),
        ('marriage', 'Marriage'),
        ('haldi', 'Haldi'),
        ('mehendi', 'Mehendi'),
        ('baby_shower', 'Baby Shower'),
        ('other', 'Other'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)  # Link Event to Venue
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    type_of_event = models.CharField(max_length=50, choices=TYPE_OF_EVENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    mode_of_payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='not_yet')
    def __str__(self):
        return f"{self.get_type_of_event_display()} at {self.venue} for {self.client}"



class Sales(models.Model):
    PAYMENT_STATUS = (
        ('received', 'Received'),
        ('not_received', 'Not Received'),
        ('partial_payment', 'Partial Payment'),
        )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    discount = models.DecimalField(max_digits = 10,decimal_places=2,default=0)
    date = models.DateField(default=timezone.now)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='not_yet')
    payment = models.CharField(max_length=20 , default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='sales')

    def __str__(self):
        return f"Sale of {self.amount} for {self.client} at {self.event}"
        
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expenses(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('received', 'Received'),
        ('not_received', 'Not Received'),
        ('partial_payment', 'Partial Payment'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online'),
        ('not_yet_decided', 'Not Yet Decided'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    particulars = models.CharField(max_length=200)
    details = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='not_paid')
    mode_of_payment = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='not_yet_decided')
    payment_made_by = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='expenses')

    def __str__(self):
        return f"{self.particulars} - {self.amount}"

class GoodsList(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_goods')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_goods')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)  # Link GoodsList to Venue
    type_of_event = models.TextField()
    event_date = models.DateField()
    event_start_at = models.DateField()
    event_end_at = models.DateField()
    day_of_event = models.TextField()
    list_of_good = models.TextField()

    def __str__(self):
        return f"{self.type_of_event} - {self.event_date}"

class EventExcel(models.Model):
    excel = models.FileField(upload_to='event_excel')

    def __str__(self):
        return self.excel.name


class EmployeeExcel(models.Model):
    excel = models.FileField(upload_to='employee_excel')

    def __str__(self):
        return self.excel.name


class DocumentOfEmployee(models.Model):
    eid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='userid')
    adharcard = models.FileField(upload_to='document/', null=True, blank=True)
    pancard = models.FileField(upload_to='document/', null=True, blank=True)
    voterid = models.FileField(upload_to='document/', null=True, blank=True)
    license = models.FileField(upload_to='document/', null=True, blank=True)
    passport = models.FileField(upload_to='document/', null=True, blank=True)

    def __str__(self):
        return f"Documents of {self.eid}"


class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    data_completion_percentage = models.PositiveIntegerField(default=0)
    selected_theme = models.CharField(max_length=20, choices=settings.THEME_CHOICES, default='light')

    def __str__(self):
        return f"Settings for {self.user}"


from django.contrib.auth import get_user_model
CustomUser = get_user_model()

class Attendance(models.Model):
    SHIFT_CHOICES = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night', 'Night')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    status = models.CharField(max_length=10, choices=(('present', 'Present'), ('absent', 'Absent')))
    marked_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendance')
    
    def __str__(self):
        return f"{self.user.username} - {self.datetime} ({self.shift}, {self.status})"




from django.db import models
from django.utils.translation import gettext_lazy as _

class Lead(models.Model):
    SOURCE_CHOICES = (
        ('online', _('Online')),
        ('offline', _('Offline')),
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='lead',  # Assuming you have a related_name specified
        verbose_name=_('Event'),  # Adjust verbose_name as needed
        null=True,  # Allow the event to be optional
        blank=True,
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('User who created the lead')
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='leads',
        verbose_name=_('Client')
    )
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='events', null=True, blank=True)

    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        verbose_name=_('Source')
    )
    reject = models.BooleanField(
        default=False,
        verbose_name=_('Rejected')
    )
    message = models.TextField(
        blank=True,
        default='remain',# Make the field optional
        verbose_name=_('Message'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    convert = models.BooleanField(
        default=False,
        verbose_name=_('Convert')
    )
    referral = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_('Referral')
    )

    class Meta:
        verbose_name = _('Lead')
        verbose_name_plural = _('Leads')

    def __str__(self):
        return f"{self.client} - {self.created_at}"

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure refer is None if not converted.
        """
        if not self.convert:
            self.referral = None
        super().save(*args, **kwargs)


class ProblemOfEmployee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    problem = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"