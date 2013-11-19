import requests
import json


from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.contrib.auth import get_user_model
User = get_user_model()

from web.models import default_country, GMDUser

from registration import signals
from registration.views import RegistrationView as BaseRegistrationView

from django_facebook.registration_backends import NooptRegistrationBackend

class RegistrationView(BaseRegistrationView, NooptRegistrationBackend):
    """
    A registration backend which implements the simplest possible
    workflow: a user supplies a username, email address and password
    (the bare minimum for a useful account), and is immediately signed
    up and logged in).
    
    """
    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']

        # facebook/connect may call this when a user already exists
        try:
            user = User.objects.get(username = username)
            return user
        except User.DoesNotExist:
            User.objects.create_user(username, email, password)



        new_user = authenticate(username=username, password=password)

        # get default country
        new_user.country = default_country(request)
        new_user.save()

        login(request, new_user)


        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)



        return new_user


    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        return ('registration_complete', (), {})
