import json
import requests

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from frontend.forms import LoginForm, RegisterForm


class LoginRequiredMixin(object):
    """
    This class acts as a mixin to enforce user authentication
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Overrides the dispatch method of the view class.

        Args: request, other arguments and key-value pairs.
        Returns: The call to the dispatch method of the parent class
                  i.e. the View class
        """
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class UserLoginView(View):
    """
    This class handles user login.

    Raw
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to the 'login' named route.

        Returns: A HTTP Response with authentication template
        """
        login_form = LoginForm()
        args = {}
        args.update(csrf(request))
        args.update({
            'login_form': login_form,
            'login_class': 'active'
        })
        return render(request, 'authenticate.html', args)

    def post(self, request, *args, **kwargs):
        """
        Process form data on POST requests
        """
        auth_form = AuthenticationForm(data=request.POST)
        import pdb; pdb.set_trace()
        if auth_form.is_valid():
            login(request, auth_form.get_user())

            url = 'http://' + request.get_host() + '/api/v1/auth/login/'
            data = {
                'username': auth_form.cleaned_data['username'],
                'password': auth_form.cleaned_data['password']
            }
            api_response = requests.post(url, json=data)
            user_token = api_response.json()['token']

            response = HttpResponseRedirect(reverse('bucketlists'))
            response.set_cookie('user_token', user_token)
            return response
        else:
            for key in auth_form.errors:
                for error in auth_form.errors[key]:
                    messages.add_message(request, messages.INFO, error)

            args = {}
            args.update(csrf(request))
            args.update({'form': RegisterForm})
            return render(
                request, 'authenticate.html', {'form': RegisterForm}
            )


class UserRegistrationView(View):
    """
    This class handles user signup.

    Raw data posted from form is received here, bound to form
    as dictionary and sent to unrendered dango form for validation.

    Returns: A HTTP Response with a register template, otherwise,
             redirects to the login page.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to the 'register' named route.
        Returns: A HTTP Response with register template.
        """
        register_form = RegisterForm()
        args = {}
        args.update(csrf(request))
        args.update({
            'register_form': register_form,
            'register_class': 'active'
        })
        return render(request, 'register.html', args)

    def post(self, request, *args, **kwargs):
        """
        Process form data on Post requests
        """
        user_form = RegisterForm(request.POST)
        import pdb; pdb.set_trace()
        # check that the username isn't already taken
        username = request.POST.get('username')
        have_same_username = User.objects.filter(username__exact=username)
        if have_same_username:
            args = {
                'register_class': 'active'
            }
            args.update(csrf(request))
            msg = ("Username is already taken. Please signup with another"
                   " username.")
            messages.add_message(request, messages.INFO, msg)
            return render(request, 'register.html', args)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            for key in user_form.errors:
                for error in user_form.errors[key]:
                    messages.add_message(request, messages.INFO, error)

            args = {}
            args.update(csrf(request))
            args.update({'form': RegisterForm})
            return render(
                request, 'register.html', {'form': RegisterForm}
            )


class BucketlistAppView(LoginRequiredMixin, View):
    """
    This view points to the bucketlist frontend app.
    Most of this section is implemented in reactJS folder.
    Here, we just render the template.
    """
    def get(self, request):
        """
        Renders the bucketlist template
        """
        return render(request, 'bucketlists.html')
