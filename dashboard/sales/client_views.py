from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from datetime import datetime
from ..models import Client, Event
from ..forms import ClientForm , EventForm
from ..authentication.permission_views import *

@login_required(login_url="/login")
@admin_or_manager_required
def client_detail(request):
    context = {}
    
    # Retrieve the client object from the database
    client = Client.objects.filter(leadperson = False)
    context['clients'] = client
    return render(request, 'client_detail.html', context)

@login_required(login_url="/login")
@admin_required
def add_client(request):
    if request.method == 'POST':
        # Retrieve data from the form
        client_name = request.POST.get('client_name')
        client_number = request.POST.get('client_number')
        client_email = request.POST.get('client_email')

        # Create a new client object in the database
        Client.objects.create(
            name=client_name,
            number=client_number,
            email=client_email
        )
        return redirect('/client_detail/')  # Assuming this URL exists
    return render(request, 'add_client.html')

@login_required(login_url="/login")
@admin_required
def update_client(request, cid):
    # Get the client object or return 404 if not found
    client = get_object_or_404(Client, id=cid)

    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            # Save the updated client
            client_form.save()
            
            return redirect('/client_detail/')  # Redirect to client list page after successful client update
    else:
        client_form = ClientForm(instance=client)
    return render(request, 'update_client.html', {'client_form': client_form})

@login_required(login_url="/login")
@admin_required
def delete_client(request,cid):
    # Delete the client object from the database
    client = Client.objects.filter(id=cid)
    client.delete()
    return redirect('/client_detail')  # Assuming this URL exists
