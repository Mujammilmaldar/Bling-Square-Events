from ..forms import EmployeeForm, DocumentOfEmployeeForm, InternForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from datetime import datetime
from ..models import CustomUser, Internship
from django.contrib import messages
# from .authentication_views import check_user
from ..forms import EmployeeForm , InternForm
from django.db.models import Q
from ..authentication.permission_views import *
@login_required(login_url="/login")
# @admin_hr_or_manager_required
@login_required
def employee_list(request):
    user = request.user

    # Determine the user's role
    user_role = user.category  # Assuming category stores the user role

    # Initialize employees queryset
    employees = CustomUser.objects.exclude(pk=user.pk)  # Exclude the currently logged-in user

    # Handle search functionality for employees
    search_query = request.GET.get('q', '')  # Set default value to empty string if search_query is None
    if search_query:
        employees = employees.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(dob__icontains=search_query) |
            Q(joiningdate__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(designation__icontains=search_query) |
            Q(mobileno__icontains=search_query)
        )

    # Further filter employees based on user role
    if user_role == 'hr':
        employees = employees.filter(category='employee')
    elif user_role == 'manager':
        employees = employees.filter(category='employee', designation='Manager')
    elif user_role != 'admin':
        employees = CustomUser.objects.none()
        
    # Initialize interns queryset
    interns = CustomUser.objects.filter(category='intern')

    # Handle search functionality for interns
    search_query2 = request.GET.get('q2', '')  # Set default value to empty string if search_query is None
    if search_query2:
        interns = interns.filter(
            Q(username__icontains=search_query2) |
            Q(email__icontains=search_query2) |
            Q(gender__icontains=search_query2) |
            Q(dob__icontains=search_query2) |
            Q(joiningdate__icontains=search_query2) |
            Q(address__icontains=search_query2) |
            Q(mobileno__icontains=search_query2)
        )

    context = {
        'name': 'Employees',
        'user': user,
        'employees': employees,
        'employee': interns,  # Use 'interns' instead of 'employee'
        'search_query': search_query,
        'search_query2': search_query2,
    }
    return render(request, 'employee_list.html', context)

@login_required(login_url="/login")
# @admin_hr_or_manager_required
def intern_list(request):
    user = request.user

    # Determine the user's role
    user_role = user.category  # Assuming category stores the user role

    # Initialize interns queryset
    interns = CustomUser.objects.filter(category='intern')

    # Handle search functionality
    search_query = request.GET.get('q', '')  # Set default value to empty string if search_query is None
    if search_query:
        interns = interns.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(dob__icontains=search_query) |
            Q(joiningdate__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(mobileno__icontains=search_query)
        )

    context = {
        'name':'inters',
        'user': user,
        'employees': interns,
        'search_query': search_query,
    }
    return render(request, 'employee_list.html', context)


def check(request):
    doc = DocumentOfEmployee.objects.all()
    context={'doc':doc}
    return render(request,'check.html',context)
    

from django.shortcuts import get_object_or_404
@login_required(login_url="/login")
@admin_hr_or_manager_required
def update_employee(request,eid):
    # If emp_id is provided, retrieve the employee object
    if eid:
        employee = get_object_or_404(CustomUser, id=eid)
    else:
        employee = None

    if request.method == 'POST':
        # Extract form data directly from request.POST
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        photo = request.FILES.get('photo')
        gender = request.POST['gender']
        dob = request.POST['dob']
        joiningdate = request.POST['joiningdate']
        address = request.POST['address']
        designation = request.POST['designation']
        mobileno = request.POST['mobileno']
        active = request.POST.get('active')  
        if active == 'True':
            active = True
        else:
            active = False  # Check if active checkbox is checked

        if employee:
            # If employee exists, it's an update operation
            employee.username = username
            employee.first_name = first_name
            employee.last_name = last_name
            employee.email = email
            if password:  # Only update password if it's provided
                employee.set_password(password)
            if photo:
                employee.photo = photo
            employee.gender = gender
            employee.dob = dob
            employee.joiningdate = joiningdate
            employee.address = address
            employee.designation = designation
            employee.mobileno = mobileno
            employee.active = active
            employee.save()

            # Update document uploads (if any)
            document, created = DocumentOfEmployee.objects.get_or_create(eid=employee)
            if request.FILES.get('adharcard'):
                document.adharcard = request.FILES['adharcard']
            if request.FILES.get('pancard'):
                document.pancard = request.FILES['pancard']
            if request.FILES.get('voterid'):
                document.voterid = request.FILES['voterid']
            if request.FILES.get('license'):
                document.license = request.FILES['license']
            if request.FILES.get('passport'):
                document.passport = request.FILES['passport']
            document.save()
                # Optionally, you can add messages or perform other actions here
            messages.success(request, 'Employee updated successfully.')
            return redirect('/Employee_List/')  # Redirect to a success URL after form submission
    
    return render(request, 'update_emp.html', {'emp': employee})



def employee_detail(req,eid):
    detail = CustomUser.objects.get(id=eid)
    context={
        'employee': detail,
    }
    context={}
    return render(req,'employee_detail.html',context)

@login_required(login_url="/login")
@admin_hr_or_manager_required
def update_intern(request, intern_id):
    if request.method == 'POST':
        intern = CustomUser.objects.get(id=intern_id)
        
        # Retrieve form data from the request
        photo = request.FILES.get('photo')
        address = request.POST.get('address')
        designation = request.POST.get('designation')
        mobileno = request.POST.get('mobileno')
        active = request.POST.get('active')

        # Update intern instance with form data
        if photo:
            intern.photo = photo
        intern.address = address
        intern.designation = designation
        intern.mobileno = mobileno
        intern.active = active

        # Save the updated intern instance
        intern.save()

        messages.success(request, 'Intern details updated successfully.')
        return redirect('intern_detail', intern_id=intern.id)
    else:
        # Handle GET request when form is initially loaded
        intern = CustomUser.objects.get(id=intern_id)
        context = {'intern': intern}
        return render(request, 'update_intern.html', context)
    
    

from ..forms import EmployeeForm, DocumentOfEmployeeForm
from django.db import transaction
from ..models import DocumentOfEmployee

@transaction.atomic
@login_required(login_url="/login")
# @admin_or_hr_required
def add_employee(request):
    if request.method == 'POST':
        # Extract form data directly from request.POST
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        photo = request.FILES.get('photo')
        gender = request.POST['gender']
        dob = request.POST['dob']
        joiningdate = request.POST['joiningdate']
        address = request.POST['address']
        designation = request.POST['designation']
        mobileno = request.POST['mobileno']
        active = request.POST.get('active')  
        if active == 'True':
            active = True
        else:
            active = False  # Check if active checkbox is checked

        # Create and save CustomUser instance
        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            photo=photo,
            gender=gender,
            dob=dob,
            joiningdate=joiningdate,
            address=address,
            designation=designation,
            mobileno=mobileno,
            active=active,
        )

        # Handle document uploads
        document = DocumentOfEmployee(eid=user)
        document.adharcard = request.FILES.get('adharcard')
        document.pancard = request.FILES.get('pancard')
        document.voterid = request.FILES.get('voterid')
        document.license = request.FILES.get('license')
        document.passport = request.FILES.get('passport')
        document.save()

        # Optionally, you can add messages or perform other actions here
        messages.success(request, 'Employee added successfully.')

        return redirect('/Employee_List/')  # Redirect to a success URL after form submission

    return render(request, 'add_employee.html')




@login_required(login_url="/login")
# @admin_or_hr_required
def add_intern(request):
    if request.method == 'POST':
        # Extract data from request.POST
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        joiningdate = request.POST.get('joiningdate')
        address = request.POST.get('address')
        designation = request.POST.get('designation')
        mobileno = request.POST.get('mobileno')
        active = request.POST.get('active') 
        if active == 'True':
            active = True
        else:
            active = False  # Convert 'True'/'False' to boolean

        # Additional intern fields
        end_date = request.POST.get('end_date')

        # Create CustomUser instance
        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            photo=photo,
            gender=gender,
            dob=dob,
            joiningdate=joiningdate,
            address=address,
            designation=designation,
            mobileno=mobileno,
            active=active,
        )

        # Create Internship instance
        intern = Internship.objects.create(intern=user, start_date=joiningdate, end_date=end_date)
        
        document = DocumentOfEmployee(eid=user)
        document.adharcard = request.FILES.get('adharcard')
        document.pancard = request.FILES.get('pancard')
        document.voterid = request.FILES.get('voterid')
        document.license = request.FILES.get('license')
        document.passport = request.FILES.get('passport')
        document.save()
        
        # Optionally, you can add messages or perform other actions here
        messages.success(request, 'Intern added successfully.')

        return redirect('/Employee_List/')  # Redirect to a success URL after form submission

    return render(request,'add_intern.html')


