from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import Venue
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import VenueForm
from ..authentication.permission_views import *
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
# @admin_or_manager_required
def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/venue_list')  # Redirect to venue list page upon successful form submission
    else:
        form = VenueForm()
    return render(request, 'add_venue.html', {'form': form})
@login_required(login_url="/login")
# @admin_or_manager_required
def venue_list(request):
    venues = Venue.objects.all()
    return render(request, 'venue_list.html', {'venues': venues})

@login_required(login_url="/login")
@admin_required
def delete_venue(request, vid):
    try:
        Venue.objects.delete(id=vid)    
        return redirect('venue_list')  # Assuming 'venue_list' is the name of your venue list URL pattern
    except Exception as e:
        return HttpResponse('error')

from django.shortcuts import render, redirect, get_object_or_404
from ..forms import VenueForm
from ..models import Venue

@login_required(login_url="/login")
# @admin_or_manager_required
def edit_venue(request, eid):
    venue = get_object_or_404(Venue, id=eid)
    if request.method == 'POST':
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('venue_list')  # Assuming 'venue_list' is the name of your venue list URL pattern
    else:
        form = VenueForm(instance=venue)  # Pass the instance here

    return render(request, 'edit_venue.html', {'form': form, 'venue': venue})
