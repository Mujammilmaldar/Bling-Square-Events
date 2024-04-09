# middleware.py

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        
        # Apply theme based on preference stored in the request
        if 'theme' in request.COOKIES:
            theme = request.COOKIES['theme']
            if theme == 'dark':
                response.set_cookie('theme', 'dark')
            else:
                response.set_cookie('theme', 'light')
        else:
            # Default theme
            response.set_cookie('theme', 'light')

        return response
