from ..forms import ProblemOfEmployeeForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from finish import settings
# from .authentication_views import check_user  # Importing the check_user decorator
from ..models import CustomUser, UserSettings 
from django.utils.translation import activate
from ..authentication.permission_views import *
from django.http import JsonResponse

@login_required(login_url="/login")
def change_language(request):
    if request.method == 'POST' and 'language' in request.POST:
        language = request.POST.get('language')
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        user_settings.language = language
        user_settings.save()
        activate(language)
        # Optionally, you can set a success message or perform other actions
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required(login_url="/login")
def settings_page(request):
    return render(request, 'settings.html')


@login_required(login_url="/login")
def profile(request):
    us = request.user
    if request.method == 'POST' and 'language' in request.POST:
        return change_language(request)

    user = request.user
    user_settings, created = UserSettings.objects.get_or_create(user=user)

    # Define fields contributing to profile completion and their completion weightages
    profile_fields = {
        'first_name': 1,
        'last_name': 1,
        'username':1,
        'email': 1,
        'address': 2,  # Example weightages, adjust as needed
        'designation': 2,
        'photo': 2  # Adjust weightages as needed
        # Add more fields and their weightages as needed
    }

    # Calculate completion percentage based on filled profile fields
    total_weightage = sum(profile_fields.values())
    filled_weightage = sum(profile_fields[field] for field in profile_fields if getattr(user, field))
    completion_percentage = int((filled_weightage / total_weightage) * 100)

    # Update user's data_completion_percentage field in UserSettings
    user_settings.data_completion_percentage = completion_percentage
    user_settings.save()

    context = {
        'user': user,
        'completion_percentage': completion_percentage,
        'user_settings': user_settings,
        'languages': settings.LANGUAGES,
        'employee':us
        
    }
    return render(request, 'profile.html', context)


@login_required(login_url="/login")

def report_problem(request):
    if request.method == 'POST':
        form = ProblemOfEmployeeForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            # Send an email to developer
            send_mail(
                'New Problem Reported',
                form.cleaned_data['details'],  # Assuming details is the field containing problem description
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEVELOPER_EMAIL],
                fail_silently=False,
            )
            context = {'success': "Your report has been sent. We will reply soon!"}
            return render(request, 'problemreport.html', context)
    else:
        initial_data = {'summary': 'add what is your problem', 'details': request.user.email}  # Example initial data
        form = ProblemOfEmployeeForm(initial=initial_data)  # Pass initial data to the form

    return render(request, 'problemreport.html', {'form': form})
