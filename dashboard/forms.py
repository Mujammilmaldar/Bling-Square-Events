# forms.py
from django import forms
from .models import DocumentOfEmployee, Event, Client, Lead, Vendor
from django import forms
from .models import CustomUser
from django.forms.models import inlineformset_factory
class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    address = forms.CharField()
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    joiningdate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    mobileno = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'number'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'photo', 'gender', 'dob', 'joiningdate', 'address', 'designation', 'mobileno', 'active', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(key, value) for key, value in CustomUser.USER_ROLES if key != 'intern'] 

class DocumentOfEmployeeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        provided_fields = [field_name for field_name, field_value in cleaned_data.items() if field_value]
        if len(provided_fields) < 2:
            raise forms.ValidationError("At least two document fields are required.")
        return cleaned_data

    class Meta:
        model = DocumentOfEmployee
        fields = ['adharcard', 'pancard', 'voterid', 'license', 'passport']

    def is_valid(self, *args, **kwargs):
        valid = super().is_valid(*args, **kwargs)
        if not valid:
            print("Document Form Errors:", self.errors)
        return valid


from django.contrib.auth.hashers import make_password

class InternForm(EmployeeForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    
    # Document fields
    adharcard = forms.FileField(required=False)
    pancard = forms.FileField(required=False)
    voterid = forms.FileField(required=False)
    license = forms.FileField(required=False)
    passport = forms.FileField(required=False)

    class Meta(EmployeeForm.Meta):
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'photo', 'gender', 'dob', 'joiningdate', 'address', 'designation', 'mobileno', 'active', 'category', 'start_date', 'end_date', 'adharcard', 'pancard', 'voterid', 'license', 'passport']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = 'intern'  # Set default value to 'intern' for category field
    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            instance.password = make_password(password)  # Hash the password
        if commit:
            instance.save()
        return instance

from django import forms 
from .models import Event

class EventForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label='Select a client', required=False)
    new_client_name = forms.CharField(max_length=100, required=False, label='New Client Name')
    new_client_number = forms.CharField(max_length=15, required=False, label='Phone Number')
    new_client_email = forms.EmailField(required=False, label='Email')
    leadperson = forms.BooleanField(required=False, label='Lead Person')

    # Add date fields
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    EVENT_CHOICES = (
        ('marriage', 'Marriage'),
        ('haldi', 'Haldi'),
        ('mehendi', 'Mehendi'),
        ('baby_shower', 'Baby Shower'),
        ('birthday', 'Birthday'),
        ('other', 'Other')  # Add more event types as needed
        )
    type_of_event = forms.ChoiceField(choices=EVENT_CHOICES, required=False, label='Type of Event')
    

    class Meta:
        model = Event
        fields = ['client', 'new_client_name', 'new_client_number', 'new_client_email', 'venue', 'start_date', 'end_date', 'status', 'mode_of_payment', 'leadperson']
        widgets = {

            'new_client_email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_new_client_number(self):
        new_client_number = self.cleaned_data['new_client_number']
        if not new_client_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return new_client_number

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        # Add custom validation for start_date if needed
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        # Add custom validation for end_date if needed
        return end_date


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'number', 'email']

# Create an inline formset for handling the relationship between Event and Client
# EventClientFormSet = inlineformset_factory( Client,Event, form=EventForm, can_delete=False, extra=1)
from django import forms
from .models import ProblemOfEmployee

class ProblemOfEmployeeForm(forms.ModelForm):
    summary = forms.CharField(label="Summary", max_length=100)
    details = forms.CharField(label="Details", widget=forms.Textarea)

    class Meta:
        model = ProblemOfEmployee
        fields = ['summary', 'details']

    def __init__(self, *args, **kwargs):
        super(ProblemOfEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs['readonly'] = True
        self.fields['details'].widget.attrs['readonly'] = True
        self.fields['summary'].widget.attrs['class'] = 'form-control'
        self.fields['details'].widget.attrs['class'] = 'form-control'

    def set_user_info(self, user):
        self.fields['summary'].initial = f"Name: {user.first_name} {user.last_name}"
        self.fields['details'].initial = self.get_user_info(user)

    def get_user_info(self, user):
        return f"Name: {user.first_name} {user.last_name}\nEmail: {user.email}\nPhone: {user.mobileno}"  # Adjust as per your user profile model


from .models import Venue

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'capacity']
        widgets = {
            'address': forms.TextInput(),
        }




from django import forms
from .models import Vendor, Expenses
from django import forms
from .models import Vendor, Expenses

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['vendor', 'particulars', 'details', 'amount', 'payment_status', 'mode_of_payment', 'payment_made_by', 'photo']
        labels = {
            'vendor': 'Vendor',
            'particulars': 'Particulars',
            'details': 'Details',
            'amount': 'Amount',
            'payment_status': 'Payment Status',
            'mode_of_payment': 'Mode of Payment',
            'payment_made_by': 'Payment Made By',
            'photo': 'Photo'
        }
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'particulars': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'mode_of_payment': forms.Select(attrs={'class': 'form-control'}),
            'payment_made_by': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['vendor'].queryset = Vendor.objects.all()

from .models import Sales

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['client', 'amount', 'discount', 'date','payment_status','payment']
    def __init__(self, *args, **kwargs):
        super(SalesForm, self).__init__(*args, **kwargs)
        self.fields['client'].required = False

from django import forms
from django.forms.widgets import DateInput
from .models import Venue, CustomUser

from django import forms
from django.forms.widgets import DateInput
from .models import Venue, CustomUser

class LeadForm(forms.Form):
    source_choices = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    user = forms.ChoiceField(choices=[])
    source = forms.ChoiceField(choices=source_choices, required=False)
    
    # Existing Venue fields
    venue_existing = forms.ModelChoiceField(queryset=Venue.objects.all(), required=False, label='Select existing venue')
    
    # New Venue fields
    venue_name = forms.CharField(max_length=100, required=False)
    venue_address = forms.CharField(max_length=200, required=False)
    venue_capacity = forms.IntegerField(required=False)
    
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    
    EVENT_CHOICES = (
        ('marriage', 'Marriage'),
        ('haldi', 'Haldi'),
        ('mehendi', 'Mehendi'),
        ('baby_shower', 'Baby Shower'),
        ('birthday', 'Birthday'),
        ('other', 'Other')  # Add more event types as needed
    )
    type_of_event = forms.ChoiceField(choices=EVENT_CHOICES, required=False, label='Type of Event')
    
    # Client fields
    client_name = forms.CharField(max_length=100, required=False)
    client_number = forms.CharField(max_length=15, required=False, widget=forms.NumberInput(attrs={'pattern': '[0-9]{10}', 'title': 'Enter a 10-digit mobile number'}))
    client_email = forms.EmailField(required=False)
    
    # Sales fields
    date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leadperson'] = forms.BooleanField(initial=True, required=False)
        self.fields['user'].choices = self.get_user_choices()

    def get_user_choices(self):
        users = CustomUser.objects.all()
        user_choices = [(user.username, user.username) for user in users]
        return user_choices
        
    def clean_leadperson(self):
        leadperson_value = self.cleaned_data['leadperson']
        client_name = self.cleaned_data.get('client_name')
        client_number = self.cleaned_data.get('client_number')
        
        if not client_name and leadperson_value:
            raise forms.ValidationError("Leadperson cannot be True if no client is provided.")
        
        if client_name and len(client_number) < 10:
            raise forms.ValidationError("Client number must be at least 10 characters long.")
        
        return leadperson_value
