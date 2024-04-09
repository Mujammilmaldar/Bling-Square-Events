from datetime import timezone
from pyexpat.errors import messages
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from ..models import Client, Event, Lead, Sales , CustomUser, Venue
from ..forms import LeadForm, EventForm, ClientForm, SalesForm


from django.contrib.auth import get_user_model
from ..models import Lead, Client, Event, Sales,CustomUser
from django.shortcuts import render, redirect
from ..forms import LeadForm
from django.db import transaction  # Import transaction module

from django.db import transaction  # Import transaction module
from django.utils import timezone
from django.shortcuts import get_object_or_404

# @transaction.atomic
# def LeadEntry(request):
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             # Extract form data
#             source = form.cleaned_data['source']
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             type_of_event = form.cleaned_data['type_of_event']
#             client_name = form.cleaned_data['client_name']
#             client_number = form.cleaned_data['client_number']
#             client_email = form.cleaned_data['client_email']
#             date = form.cleaned_data['date']
#             leadperson = form.cleaned_data['leadperson']
            
#             # Check if the client already exists, otherwise create a new client
#             client, _ = Client.objects.get_or_create(name=client_name, defaults={'number': client_number, 'email': client_email, 'leadperson': leadperson})

#             # Check if the user selected an existing venue or entered details for a new one
#             venue_existing = form.cleaned_data['venue_existing']
#             if venue_existing:
#                 venue = venue_existing
#             else:
#                 # Create a new venue
#                 venue_name = form.cleaned_data['venue_name']
#                 venue_address = form.cleaned_data['venue_address']
#                 venue_capacity = form.cleaned_data['venue_capacity']
#                 venue = Venue.objects.create(name=venue_name, address=venue_address, capacity=venue_capacity)

#             # Create the event associated with the client and venue
#             event = Event.objects.create(venue=venue, start_date=start_date, end_date=end_date, type_of_event=type_of_event, client=client)
            
#             # Create the sales associated with the client
#             sales = Sales.objects.create(client=client, date=date)

#             # Create the lead
#             try:
#                 username = form.cleaned_data['user']
#                 user = get_object_or_404(get_user_model(), username=username)
#             except get_user_model().DoesNotExist:
#                 return HttpResponse("User does not exist", status=404)

#             lead = Lead.objects.create(user=user, source=source, client=client)

#             # Redirect to a success page or do something else
#             return redirect('/lead_list/')
#         else:
#             # Handle form validation errors
#             print("Form Errors:", form.errors)
#     else:
#         form = LeadForm()
    
#     return render(request, 'lead_entry.html', {'form': form})

def LeadEntry(request):
    if request.method == 'POST':
        # Extract data from the POST request
        user_id = request.POST.get('user')
        source = request.POST.get('source')
        venue_existing_id = request.POST.get('venue_existing')
        venue_name = request.POST.get('venue_name')
        venue_address = request.POST.get('venue_address')
        venue_capacity = request.POST.get('venue_capacity')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        type_of_event = request.POST.get('type_of_event')
        client_name = request.POST.get('client_name')
        client_number = request.POST.get('client_number')
        client_email = request.POST.get('client_email')
        leadperson = True
        date = request.POST.get('date')
        notes = request.POST.get('notes')
        referral = request.POST.get('referral')  # Added referral field

        # Process the form data and save to the database
        client, _ = Client.objects.get_or_create(name=client_name, number=client_number, email=client_email)
        
        if venue_existing_id:
            venue = Venue.objects.get(pk=venue_existing_id)
        else:
            if venue_name:  # Check if a new venue name is provided
                # Create a new Venue object with provided details
                venue = Venue.objects.create(name=venue_name, address=venue_address, capacity=venue_capacity)
            else:
                # No venue name provided for a new venue
                # messages.error(request, 'Please provide a venue name.')
                print('Please provide a venue name.')
                return redirect('lead_entry')

        event = Event.objects.create(client=client, venue=venue, start_date=start_date, end_date=end_date, type_of_event=type_of_event)
        Sales.objects.create(client=client, amount=0, date=date, payment_status='not_received', event=event)

        # Create the lead record with today's date
        lead = Lead.objects.create(user_id=user_id, client=client, source=source, referral=referral, created_at=timezone.now())

        # Optionally, you can add a success message
        # messages.success(request, 'Lead added successfully.')
        return redirect('lead_list')  # Redirect to the lead list page or any other page
    else:
        # Fetch all necessary data to pass to the template
        venues = Venue.objects.all()
        status_choices = Event.STATUS_CHOICES
        payment_choices = Event.PAYMENT_CHOICES
        type_of_event_choices = Event.TYPE_OF_EVENT_CHOICES
        user_choices = CustomUser.objects.all().values_list('id', 'username')
        SOURCE_CHOICES = Lead.SOURCE_CHOICES

        # Create the context dictionary with all the necessary data
        context = {
            'venues': venues,
            'status_choices': status_choices,
            'payment_choices': payment_choices,
            'type_of_event_choices': type_of_event_choices,
            'user_choices': user_choices,
            'source_choices': SOURCE_CHOICES,
        }

        # Render the form with the context
        return render(request, 'lead_entry.html', context)

from django.db.models import Q
def LeadList(request):
    # Initialize an empty leads queryset
    leads = Lead.objects.filter(reject=False,convert=False)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        # Filter leads based on search query
        leads = leads.filter(Q(client__name__icontains=query) | Q(message__icontains=query))
    
    # Create context data
    context = {'leads': leads, 'name': 'All', 'search_query': query}  # Pass search query to template
    
    # Pass the leads queryset and context to the template for rendering
    return render(request, 'lead_list.html', context)


def LeadCancel(request):
    # Retrieve all lead objects from the database
    leads = Lead.objects.filter(reject=True)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        # Filter leads based on search query
        leads = leads.filter(Q(client__name__icontains=query) | Q(message__icontains=query))
    
    # Create context data
    context = {'leads': leads, 'name': 'cancel', 'search_query': query}
    
    # Pass the leads queryset and context to the template for rendering
    return render(request, 'lead_list.html', context)

def ConvertedLeads(request):
    # Retrieve all converted lead objects from the database
    leads = Lead.objects.filter(convert=True)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        # Filter leads based on search query
        leads = leads.filter(Q(client__name__icontains=query) | Q(message__icontains=query))
    
    # Create context data
    context = {'leads': leads, 'name': 'Converted', 'search_query': query}
    
    # Pass the leads queryset and context to the template for rendering
    return render(request, 'lead_list.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from ..models import Event, Client, Venue, Sales

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from ..models import Event, Client, Sales

from django.shortcuts import render, redirect, get_object_or_404
from ..models import Lead, Client, Event, Venue, Sales
from django.contrib import messages
from django.utils import timezone

def UpdateLead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)

    if request.method == 'POST':
        # Retrieve data from the form
        source = request.POST.get('source')
        client_name = request.POST.get('client_name')
        client_number = request.POST.get('client_number')
        client_email = request.POST.get('client_email')
        referral = request.POST.get('referral')
        message = request.POST.get('message')
        # Additional data for Event model
        venue_id = request.POST.get('venue')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        type_of_event = request.POST.get('type_of_event')
        status = request.POST.get('status')

        # Update the lead with the new data
        lead.source = source
        lead.referral = referral
        # lead.message = message

        # Update related client information if changed
        client = lead.client
        if client_name and client_name != client.name:
            client.name = client_name
        if client_number and client_number != client.number:
            client.number = client_number
        if client_email and client_email != client.email:
            client.email = client_email

        # Update related event information if changed
        event = lead.event
        if venue_id:
            event.venue = Venue.objects.get(pk=venue_id)
        if start_date:
            event.start_date = start_date
        if end_date:
            event.end_date = end_date
        if type_of_event:
            event.type_of_event = type_of_event
        if status:
            event.status = status

        # Save the changes
        client.save()
        lead.save()
        event.save()

        # Optionally, add a success message
        messages.success(request, 'Lead updated successfully.')
        
        return redirect('/lead_list/')  # Redirect to the lead list page after update

    else:
        # Fetch lead details and related data for rendering the form
        clients = Client.objects.all()
        source_choices = Lead.SOURCE_CHOICES
        venues = Venue.objects.all()
        
        status_choices = Event.STATUS_CHOICES
        payment_choices = Event.PAYMENT_CHOICES
        type_of_event_choices = Event.TYPE_OF_EVENT_CHOICES
        user_choices = CustomUser.objects.all().values_list('id', 'username')
        print(lead.sales)

        context = {
            'lead': lead,
            'clients': clients,
            'source_choices': source_choices,
            'venues': venues,
            'status_choices': status_choices,
            'payment_choices': payment_choices,
            'type_of_event_choices': type_of_event_choices,
            'user_choices': user_choices,
        }
        
        return render(request, 'update_lead.html', context)


def leaddetail(request,lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    clients = Client.objects.all()
    source_choices = Lead.SOURCE_CHOICES
    venues = Venue.objects.all()
    
    status_choices = Event.STATUS_CHOICES
    payment_choices = Event.PAYMENT_CHOICES
    type_of_event_choices = Event.TYPE_OF_EVENT_CHOICES
    user_choices = CustomUser.objects.all().values_list('id', 'username')
    print(lead.sales)
    context = {
        'lead': lead,
        'clients': clients,
        'source_choices': source_choices,
        'venues': venues,
        'status_choices': status_choices,
        'payment_choices': payment_choices,
        'type_of_event_choices': type_of_event_choices,
        'user_choices': user_choices,
    }
        
    return render(request, 'lead_detail.html', context)



def DeleteLead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == 'POST':
        # Check if the user confirms the deletion
        if 'confirm_delete' in request.POST:
            lead.delete()
            return redirect('/lead_list/')  # Redirect to success page after successful deletion
        else:
            # If the user cancels the deletion, redirect to a different page or render a template
            return redirect('cancel_url')  # Redirect to cancel page or any other page
        
    # Render a confirmation template
    return render(request, 'lead_delete_confirm.html', {'lead': lead})

def convert_lead(request, lid):
    # Retrieve the lead object
    lead = Lead.objects.get(pk=lid)
    # Update the lead to mark it as converted
    lead.convert = True
    lead.client.leadperson = False
    lead.save()
    
    # Redirect to the lead list page
    return redirect('lead_list')

def reject_lead(request, lid):
    # Retrieve the lead object
    lead = Lead.objects.get(pk=lid)
    
    # Update the lead to mark it as rejected
    lead.reject = True
    lead.save()
    
    # Redirect to the lead list page
    return redirect('lead_list')