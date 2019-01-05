import logging
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger('app')


def show_login(request):
    """
    View: /login/
    """
    if request.user.is_authenticated:
        next_url = get_next_url(request)
        return HttpResponseRedirect(next_url)
    else:
        return render(request, 'login.html')


@require_http_methods(['POST'])
def logout_user(request):
    """
    View: /login/logout/
    """
    next_url = get_next_url(request)
    logout(request)
    message(request, 'primary', 'Successfully Logged Out.')
    request.session['login_next_url'] = next_url
    return redirect(next_url)


@require_http_methods(['POST'])
def do_auth(request):
    """
    View: /login/auth/
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
                    message(request, 'primary', 'Successfully Logged In.')
                    next_url = get_next_url(request)
                    return HttpResponseRedirect(next_url)
                else:
                    logout(request)
                    message(request, 'danger', 'Account is Disabled.')
                    return redirect('login:show')
        message(request, 'warning', 'Username and/or Password Incorrect.')
        return redirect('login:show')
    except Exception as error:
        logger.exception(error)
        message(request, 'danger', 'Unknown Authentication Error.')
        return redirect('login:show')


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


def message(request, level, message):
    """
    Easily add a success or error message
    """
    success = ['primary', 'success']
    if level in success:
        messages.add_message(request, messages.SUCCESS, message, extra_tags=level)
    else:
        messages.add_message(request, messages.WARNING, message, extra_tags=level)
