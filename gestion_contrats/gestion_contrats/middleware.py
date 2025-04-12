# gestion_contrats/middleware.py
from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class AuthRequiredMiddleware(MiddlewareMixin):
    exempt_url_names = [
        'login', 
        'admin:index',
        'admin:login',
        'password_reset',
        'password_reset_done',
        'password_reset_confirm',
        'password_reset_complete'
    ]

    def process_request(self, request):
        current_url_name = resolve(request.path_info).url_name
        logger.debug(f"Checking access to: {current_url_name} - Authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated:
            if current_url_name not in self.exempt_url_names:
                logger.warning(f"Unauthorized access attempt to {request.path}")
                return redirect(f"{reverse('login')}?next={request.path}")