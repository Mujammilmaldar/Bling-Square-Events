from django.contrib import messages
from ..forms import EventForm, ClientForm, SalesForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Event, Client , Lead , Sales, Venue
from datetime import datetime
from django.db.models import Q
# from .authentication_views import check_user
from django.utils import timezone
from ..authentication.permission_views import *

from django.utils import timezone
@login_required(login_url="/login")
# @admin_or_manager_required
def upcoming_events(request):
    context = {}
    search_query = request.GET.get('q', '').strip()  # Get the search query from the request and remove whitespace
    now = timezone.now().date()  # Get the current date
    
    # Define fields to search against
    search_fields = ['client__name', 'venue__name', 'type_of_event', 'status', 'mode_of_payment']
    
    # Initialize an empty query
    query = Q()
    
    # Add search conditions for each field
    for field in search_fields:
        query |= Q(**{f'{field}__icontains': search_query})
    
    # Filter events based on search query and upcoming start date
    upcoming_events = Event.objects.filter(query, start_date__gt=now).select_related('client', 'venue')
    
    context['name'] = 'upcoming events'
    context['events'] = upcoming_events
    context['search_query'] = search_query  # Pass the search query to the template
    
    return render(request, "all_events.html", context)

@login_required(login_url="/login")
# @admin_or_manager_required
def ongoing_events(request):
    context = {}
    search_query = request.GET.get('q', '').strip()  # Get the search query from the request and remove whitespace
    now = timezone.now().date()  # Get the current date without the time component

    if search_query:
        ongoing_events = Event.objects.filter(start_date__lte=now, end_date__gte=now, client__name__icontains=search_query, status__iexact='ongoing').select_related('client')
    else:
        ongoing_events = Event.objects.filter(start_date__lte=now, end_date__gte=now, status__iexact='ongoing').select_related('client')

    context['name'] = 'ongoing events'
    context['events'] = ongoing_events
    context['search_query'] = search_query  # Pass the search query to the template
    return render(request, "all_events.html", context)


from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
# @login_required(login_url="/login")
# @admin_requireddef 
# def add_event(request):
#     try:
#         if request.method == 'POST':
#             event_form = EventForm(request.POST)
#             sales_form = SalesForm(request.POST)
#             if event_form.is_valid() and sales_form.is_valid():
#                 event = event_form.save(commit=False)
#                 new_client_name = event_form.cleaned_data.get('new_client_name')
#                 new_client_number = event_form.cleaned_data.get('new_client_number')
#                 new_client_email = event_form.cleaned_data.get('new_client_email')

#                 if event.client_id:  # Check if client_id exists
#                     client = event.client
#                 elif new_client_name and new_client_number and new_client_email:
#                     new_client = Client.objects.create(
#                         name=new_client_name,
#                         number=new_client_number,
#                         email=new_client_email,
#                         bookings_count=1
#                     )
#                     client = new_client
#                     event.client = client

#                     client.bookings_count += 1
#                     client.save()

#                     event.save()

#                     sales = sales_form.save(commit=False)
#                     sales.client = client
#                     sales.save()

#                 return redirect('/All_Events')
#             else:
#                 event_form_errors = event_form.errors.as_data()
#                 sales_form_errors = sales_form.errors.as_data()
#                 print("Event Form Errors:", event_form_errors)
#                 print("Sales Form Errors:", sales_form_errors)
#         else:
#             event_form = EventForm()
#             sales_form = SalesForm()

#         return render(request, 'add_event.html', {'event_form': event_form, 'sales_form': sales_form})

#     except Exception as e:
#         # Handle exceptions gracefully
#         print("An error occurred:", str(e))
#         # Render an error page or redirect to a relevant page
#         return render(request, 'error.html', {'error_message': 'An error occurred. Please try again later.'})

from django.shortcuts import render, redirect
from ..models import Event, Sales, Venue
from django.utils import timezone

from django.db import transaction

@transaction.atomic
def add_event(request):
    if request.method == 'POST':
        # Retrieve necessary data from POST request
        venue_name = request.POST.get('venue')
        client_name = request.POST.get('client')
        sales_amount = request.POST.get('amount')

        # Check if required fields are present
        if venue_name and client_name and sales_amount:
            # Retrieve or create Venue instance
            if venue_name == 'other':
                venue_data = {
                    'name': request.POST.get('new_venue_name'),
                    'address': request.POST.get('new_venue_address'),
                    'capacity': request.POST.get('new_venue_capacity'),
                }
                venue = Venue.objects.create(**venue_data)
            else:
                venue = Venue.objects.get(pk=venue_name)

            # Retrieve or create Client instance
            if client_name == 'other':
                new_client_data = {
                    'name': request.POST.get('new_client_name'),
                    'number': request.POST.get('new_client_number'),
                    'email': request.POST.get('new_client_email'),
                }
                client = Client.objects.create(**new_client_data)
            else:
                client = Client.objects.get(pk=client_name)

            # Create Event instance
            event_data = {
                'client': client,
                'venue': venue,
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'type_of_event': request.POST.get('type_of_event'),
                'status': request.POST.get('status'),
                'mode_of_payment': request.POST.get('mode_of_payment'),
            }
            event = Event.objects.create(**event_data)

            # Create Sales instance
            sales_data = {
                'client': client,
                'amount': sales_amount,
                'discount': request.POST.get('discount'),
                'date': request.POST.get('date'),
                'payment_status': request.POST.get('payment_status'),
                'payment': request.POST.get('payment'),
                'event': event,
            }
            sales = Sales.objects.create(**sales_data)

            # Redirect upon successful creation
            return redirect('/All_Events')

        else:
            # Handle case where required fields are missing
            return HttpResponse("Error: Missing required fields.", status=400)
    else:
        venues = Venue.objects.all()  # Fetch all venues to pass to the template
        status_choices = Event.STATUS_CHOICES
        payment_choices = Event.PAYMENT_CHOICES
        type_of_event_choices = Event.TYPE_OF_EVENT_CHOICES  # Fetch all venues to pass to the template
        event = Event.objects.all()
        sales = Sales.objects.all()
        payment_status = Sales.PAYMENT_STATUS
        client =Client.objects.all()
        
        context={
            'events':event, 
            'venues': venues,
            'clients':client,
            'status_choices': status_choices,
            'payment_choices': payment_choices,
            'type_of_event_choices': type_of_event_choices, 
            'payment_status':payment_status,
             }
        
        return render(request, 'add_event.html',context)


@login_required(login_url="/login")
# @admin_required
def delete_event(request, eid):
    # Delete the event object
    event = Event.objects.get(id=eid)
    event.delete()
    return redirect('/All_Events')

# @login_required(login_url="/login")
# @admin_required
# def lead_entry(request):
#     if request.method == 'POST':
#         # Extract form data from request
#         client_name = request.POST.get('client_name')
#         contact_number = request.POST.get('contact_number')
#         email = request.POST.get('email')
#         source = request.POST.get('source')
#         message = request.POST.get('message')

#         # Create a new Lead object and save it
#         lead = Lead.objects.create(
#             client_name=client_name,
#             contact_number=contact_number,
#             email=email,
#             source=source,
#             message=message
#         )
#         return redirect('/lead_listing')  # Redirect to lead listing page after submission
#     else:
#         return render(request, 'lead_entry.html')  # Render the lead entry form

from django.forms import formset_factory
from ..forms import EventForm, ClientForm, ExpenseForm
from ..models import Event, Client, Vendor, Expenses
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from ..models import Event, Client, Sales
@login_required(login_url="/login")
# @admin_required

def update_event(request, eid):
    event = get_object_or_404(Event, id=eid)
    clients=event.client
    client = get_object_or_404(Client, id=event.client.id)
    sales = Sales.objects.get(client=clients)
    venues = Venue.objects.all()
    venue = event.venue

    if request.method == 'POST':
        try:
            # Retrieve data from POST request
            event.start_date = request.POST.get('start_date')
            event.end_date = request.POST.get('end_date')
            event.status = request.POST.get('status')
            event.mode_of_payment = request.POST.get('mode_of_payment')
            event.type_of_event = request.POST.get('type_of_event')
            
            client.name = request.POST.get('client_name')
            client.number = request.POST.get('client_number')
            client.email = request.POST.get('client_email')

            amount = request.POST.get('amount')
            discount = request.POST.get('discount')
            date = request.POST.get('date')
            payment_status = request.POST.get('payment_status')
            payment = request.POST.get('payment')
            
            # Validate and save event
            event.full_clean()
            event.save()

            # Validate and save client
            client.full_clean()
            client.save()

            # Create or update sales data
            if amount and discount and date:
                if not sales:
                    sales = Sales(event=event, client=client)
                sales.amount = amount
                sales.discount = discount
                sales.date = date
                sales.payment_status = payment_status
                sales.payment = payment
                sales.full_clean()
                sales.save()

            return redirect('/All_Events')  # Redirect to success page upon successful update

        except (ValueError, ValidationError) as e:
            return HttpResponseBadRequest("Error: " + str(e))

    else:
        print(sales)
        print(sales.amount,sales.discount)
        context = {
            'event': event,
            'client': client,
            'sales': sales,
            'venues':venues,
            'venue': venue,
            'start_date': event.start_date,
            'end_date': event.end_date,
        }
        return render(request, 'update_event.html', context)

from ..functionality.excel_views import import_data
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
from datetime import timedelta

@login_required(login_url="/login")
# @admin_or_manager_required

def all_events(request):
    if request.method == 'POST' and request.FILES.get('excel'):
        import_data(request)
    
    context = {}
    search_query = request.GET.get('q', '').strip()
    search_fields = ['client__name', 'venue__name', 'type_of_event', 'status', 'mode_of_payment']
    query = Q()
    
    if search_query:
        for field in search_fields:
            query |= Q(**{f'{field}__icontains': search_query})
        
        all_events = Event.objects.filter(query).select_related('client')
    else:
        all_events = Event.objects.all().select_related('client')
    
    # date_filter = request.GET.get('date_filter')
    # if date_filter:
    #     today = timezone.now().date()
    #     if date_filter == '1_month':
    #         start_date = today - timedelta(days=30)
    #         end_date = today
    #     elif date_filter == '2_months':
    #         start_date = today - timedelta(days=60)
    #         end_date = today
    #     elif date_filter == 'custom':
    #         start_date = request.GET.get('start_date')
    #         end_date = request.GET.get('end_date')
    #         all_events = all_events.filter(date__range=[start_date, end_date])
    
    # else:
    #     start_date = None  # Default start date
    #     end_date = timezone.now().date()  # Default end date
    print(all_events)
    context['name'] = 'all events'
    context['events'] = all_events
    context['search_query'] = search_query
    # context['date_filter'] = date_filter
    # context['start_date'] = start_date
    # context['end_date'] = end_date
    
    return render(request, "all_events.html", context)


from django.shortcuts import render, get_object_or_404
from ..models import Event, Sales, Expenses

def event_detail(request, eid):
    # Get the event object or return 404 if not found
    event = get_object_or_404(Event, id=eid)

    # Get the associated client
    client = event.client

    # Get the sales associated with the client
    sales = Sales.objects.filter(client=client)

    # Get the expenses associated with the event
    expenses = Expenses.objects.filter(event=event)

    return render(request, 'event_detail.html', {'event': event, 'client': client, 'sales': sales, 'expenses': expenses})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Expenses, Event

def add_expense(request, eid):
    event = get_object_or_404(Event, id=eid)
    vendors = Vendor.objects.all()  # Fetch all vendors for dropdown menu
    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')  # Get the vendor name from the form
        if vendor_name:  # Check if a new vendor name is provided
            # Create a new vendor instance
            vendor = Vendor.objects.create(name=vendor_name, organization_name="")
        else:
            vendor_id = request.POST.get('vendor')  # Get selected vendor ID
            vendor = get_object_or_404(Vendor, id=vendor_id)

        particulars = request.POST.get('particulars')
        details = request.POST.get('details')
        amount = request.POST.get('amount')
        payment_status = request.POST.get('payment_status')
        mode_of_payment = request.POST.get('mode_of_payment')
        payment_made_by = request.POST.get('payment_made_by')
        photo = request.FILES.get('photo')

        # Validate input
        if not (particulars and amount):
            messages.error(request, 'Please fill in all required fields.')
        else:
            # Create and save the expense
            expense = Expenses.objects.create(
                event=event,
                vendor=vendor,
                particulars=particulars,
                details=details,
                amount=amount,
                payment_status=payment_status,
                mode_of_payment=mode_of_payment,
                payment_made_by=payment_made_by,
                photo=photo
            )
            messages.success(request, 'Expense added successfully!')
            return redirect('add_expense', eid=eid)  # Redirect to the same page to clear the form

    return render(request, 'add_expenses.html', {'event': event, 'vendors': vendors})
