from django.shortcuts import render
from django.utils import timezone
from ..models import DocumentOfEmployee, Event, UserSettings

def get_user_settings(user):
    # Attempt to retrieve user settings
    user_settings, created = UserSettings.objects.get_or_create(user=user)
    return user_settings

def calculate_completion_percentage(user, profile_fields):
    try:
        documents = DocumentOfEmployee.objects.get(eid=user.id)
    except DocumentOfEmployee.DoesNotExist:
        documents = None

    # Calculate completion percentage for profile fields
    total_profile_weightage = sum(profile_fields.values())
    filled_profile_weightage = sum(profile_fields[field] for field in profile_fields if getattr(user, field))
    profile_completion_percentage = int((filled_profile_weightage / total_profile_weightage) * 100)

    # Calculate completion percentage for document fields
    if documents:
        filled_document_weightage = sum(1 for field in ['adharcard', 'pancard', 'voterid', 'license', 'passport'] if getattr(documents, field))
        total_document_weightage = 2  # Assuming equal weightage for any two documents
        document_completion_percentage = int((filled_document_weightage / total_document_weightage) * 100)
    else:
        document_completion_percentage = 0  # No documents available

    # Calculate overall completion percentage
    overall_completion_percentage = (profile_completion_percentage + document_completion_percentage) / 2  # Average of profile and document completion percentages

    return overall_completion_percentage
def update_user_settings(user_settings, completion_percentage):
    # Update user's data_completion_percentage field in UserSettings
    user_settings.data_completion_percentage = completion_percentage
    user_settings.save()

def get_progress_color(completion_percentage):
    # Define color thresholds based on completion percentage
    if completion_percentage < 30:
        return 'red'
    elif completion_percentage < 60:
        return 'orange'
    elif completion_percentage < 90:
        return 'yellow'
    else:
        return 'green'

def get_completed_events():
    # Count completed events
    return Event.objects.filter(status='completed').count()

def get_ongoing_events():
    # Get the current date
    current_date = timezone.now().date()
    
    # Filter ongoing events
    ongoing_events = Event.objects.filter(start_date__lte=current_date, status='scheduled')

    # Update status of ongoing events whose start date is today
    for event in ongoing_events:
        if event.start_date == current_date:
            event.status = 'ongoing'
            event.save()

    # Fetch ongoing events again including the ones whose status has been updated
    return Event.objects.filter(status='ongoing')[:5]