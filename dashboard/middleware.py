from django.utils.translation import activate

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.session.get('django_language')
        if language:
            activate(language)
        return self.get_response(request)

from django.utils.translation import activate
from .models import UserLanguage  # Adjust the import path as per your project structure


class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_language = UserLanguage.objects.get(user=request.user).language
                activate(user_language)
            except UserLanguage.DoesNotExist:
                pass
        response = self.get_response(request)
        return response

# middleware.py

from django.utils.translation import activate
from .models import UserSettings
class UserThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                user_settings = UserSettings.objects.get(user=request.user)
                request.session['theme'] = user_settings.selected_theme
            except UserSettings.DoesNotExist:
                # Handle the case when user settings are not found
                # For example, set a default theme or log the exception
                pass
        response = self.get_response(request)
        return response
