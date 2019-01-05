import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

logger = logging.getLogger('app')


@login_required
def home(request):
    """
    View: /
    """
    return render(request, 'home/home.html')


# AUTHENTICATION

def show_login(request):
    """
    View: /login/
    """
    if request.user.is_authenticated:
        next_url = get_next_url(request)
        return HttpResponseRedirect(next_url)
    else:
        return render(request, 'home/login.html')


@require_http_methods(['POST'])
def do_auth(request):
    """
    View: /authenticate/
    """
    try:
        _ad_user = request.POST['adUser']
        _ad_pass = request.POST['adPass']

        if 'login_next_url' not in request.session:
            login_next_url = get_next_url(request)
            request.session['login_next_url'] = login_next_url

        if _ad_user and _ad_pass:
            user_auth = authenticate(username=_ad_user, password=_ad_pass)
            if user_auth is not None:
                if user_auth.is_active:
                    login(request, user_auth)
                    message(request, 'success', 'Successfully Logged In.')
                    next_url = get_next_url(request)
                    return HttpResponseRedirect(next_url)
                else:
                    logout(request)
                    message(request, 'danger', 'Account is Disabled.')
                    return redirect('login')

        message(request, 'danger', 'Username and/or Password Incorrect.')
        return redirect('login')
    except Exception as error:
        logger.info('wtf')
        logger.exception(error)
        message(request, 'danger', 'Unknown Authentication Error.')
        return redirect('login')


@require_http_methods(['POST'])
def logout_user(request):
    """
    View: /logout/
    """
    next_url = get_next_url(request)
    logout(request)
    message(request, 'success', 'Successfully Logged Out.')
    request.session['login_next_url'] = next_url
    return redirect('login')


def get_next_url(request):
    """
    Determine next url
    """
    try:
        next_url = request.GET['next']
    except Exception:
        try:
            next_url = request.POST['next']
        except Exception:
            try:
                next_url = request.session['login_next_url']
            except Exception:
                next_url = '/'
    return next_url if next_url else '/'


def message(request, type, message):
    """
    Easily add a success or error message
    """
    if type == 'success':
        messages.add_message(request, messages.SUCCESS, message, extra_tags='success')
    if type == 'error':
        messages.add_message(request, messages.WARNING, message, extra_tags='danger')
