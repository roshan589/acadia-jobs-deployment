from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class CheckParentExpiryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if getattr(request.user, 'user_type', None) == 'parent':
                if hasattr(request.user, 'isParentAccountValid') and not request.user.isParentAccountValid():
                    logout(request)
                    messages.error(request, "Your parent account has expired.")
                    return redirect('login')
        return None
