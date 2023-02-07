from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View, TemplateView

from config import constants
from .utils import *
from markets.models import Currency



class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            return {'user': self.request.user}


class LoginView(View):
    template_name = 'website/login.html'
    templates = {'success': 'website/home.html', 'fail': 'website/login_failed.html'}
    form = AuthenticationForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        context = self.get_context_data()
        if user is not None:
            request.session.set_expiry(87400)
            login(request, user)
            return render(request, self.templates['success'], context)
        else:
            return render(request, self.templates['fail'], context)

    def get_context_data(self, **kwargs):
        return {'form': self.form}


def log_in(request):
    if request.method == 'POST' and 'password' in request.POST:
        print(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        print(user)
        if user is not None:
            request.session.set_expiry(86400)
            login(request, user)
            context = {'user': user}
            return render(request, 'website/home.html', context)
        else:
            context = {'form': AuthenticationForm}
            return render(request, 'website/login_failed.html', context)
    else:
        return render(request, 'website/login.html', {'form': AuthenticationForm})


class SignUpView(TemplateView):
    template_name = 'website/signup.html'
    templates = {'success': 'website/home.html', 'fail': 'website/signup_failed.html'}
    form = UserCreationForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = self.form(request.POST)
        context = self.get_context_data(**kwargs)
        if user_form.is_valid():
            form_data = user_form.cleaned_data
            user = User.objects.create_user(username=form_data['username'], password=form_data['password1'])
            if user:
                try:
                    setup_account(request, user)
                    login(request, user)
                    return render(request, self.templates['success'])
                except Exception as e:
                    print(f'Exception: {e}')
        else:
            print(f'errors: {user_form.errors}')
        return render(request, self.templates['fail'], context)

    def get_context_data(self, **kwargs):
        currencies = constants.SORTED_CURRENCIES
        return {'signup_form': self.form, 'currencies': currencies}




def signup(request):
    context = {'form': UserCreationForm, 'currencies': Currency.objects.all()}

    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            form_data = user_form.cleaned_data
            user = User.objects.create_user(username=form_data['username'], password=form_data['password1'])
            request.session.set_expiry(86400)
            login(request, user)
            setup_account(request)
            return render(request, 'website/home.html', context)

        else:
            print(user_form.errors)
            context['errors'] = dict(user_form.errors)
            print(context['errors'])
            return render(request, 'website/signup_failed.html', context)

    else:
        return render(request, 'website/signup.html', context)


class LogoutView(View):
    template_name = 'website/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)


def log_out(request):
    logout(request)
    return render(request, 'website/logout.html')


