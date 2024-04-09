from finish import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import CustomUser, Event, Lead, UserSettings
# from .permission_views import *
from django.utils import timezone
from datetime import timedelta
from ..functionality.homefunction_views import *


def login_page(req):
    if req.method == 'POST':
        uname = req.POST.get('uname')
        upass = req.POST.get('upass')
        context = {}
        
        # Authenticate user
        user = authenticate(username=uname, password=upass)
        if user is not None:
            # Login the user
            login(req, user)
            print("Logged in user:", user)
            # Redirect to the home page after successful login
            return redirect('/home')
        else:
            # Check if username is incorrect
            if not uname:
                context['errormsg'] = "Username is required!"
            # Check if password is incorrect
            elif not upass:
                context['errormsg'] = "Password is required!"
            else:
                context['errormsg'] = "Invalid username or password!"
            return render(req, 'login.html', context)
    else:
        # Render the login page for GET requests
        return render(req, "login.html")

@login_required(login_url="/login")
def logout_page(req):
    logout(req)
    return redirect('/login')

from django.http import JsonResponse
from django.utils.translation import activate
from django.shortcuts import render
from ..models import DocumentOfEmployee, Lead
@login_required(login_url="/login")
def home_page(request):
    user = request.user

    profile_fields = {
        'first_name': 1,
        'last_name': 1,
        'username': 1,
        'email': 1,
        'address': 2,
        'designation': 2,
        'photo': 2
        # Add more fields and their weightages as needed
    }
    
    # Calculate completion percentage
    completion_percentage = calculate_completion_percentage(user, profile_fields)
    
    # Get progress color based on completion percentage
    progress_color = get_progress_color(completion_percentage)
    
    # Fetch completed events, ongoing events, and leads
    completed_events = get_completed_events()
    ongoing_events = get_ongoing_events()
    leads = Lead.objects.order_by('-created_at')[:5]

    # Additional code to calculate document completion percentage
    try:
        documents = DocumentOfEmployee.objects.get(eid=user.id)
    except DocumentOfEmployee.DoesNotExist:
        documents = None

    if documents:
        filled_document_weightage = sum(1 for field in ['adharcard', 'pancard', 'voterid', 'license', 'passport'] if getattr(documents, field))
        total_document_weightage = 2  # Assuming equal weightage for any two documents
        document_completion_percentage = int((filled_document_weightage / total_document_weightage) * 100)
    else:
        document_completion_percentage = 0  # No documents available

    # Calculate overall completion percentage
    overall_completion_percentage = (completion_percentage + document_completion_percentage) / 2
    user_settings = get_user_settings(user)
    context = {
        'completed_events': completed_events,
        'user_settings': user_settings,
        'completion_percentage': overall_completion_percentage,
        'progress_color': progress_color,
        'events': ongoing_events,
        'leads': leads
    }

    return render(request, "home.html", context)
