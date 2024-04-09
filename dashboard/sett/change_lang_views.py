# views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from finish import settings
from ..models import UserLanguage
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from ..models import UserLanguage

@login_required
def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            UserLanguage.objects.update_or_create(user=request.user, defaults={'language': language})
    return HttpResponseRedirect(reverse('home'))



from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..models import UserSettings
from django.shortcuts import HttpResponseRedirect, reverse
from django.shortcuts import redirect

@login_required
def change_theme(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        if theme in ['light', 'dark']:
            user_settings, created = UserSettings.objects.get_or_create(user=request.user)
            user_settings.selected_theme = theme
            user_settings.save()
    return redirect(reverse('home'))
