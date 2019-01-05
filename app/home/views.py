import logging
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from home.models import Tools
from login.views import message

logger = logging.getLogger('app')


def dashboard(request):
    """
    View: /
    """
    tools = Tools.objects.get_active()
    data = {'tools': tools}
    return render(request, 'dashboard.html', data)


def about(request):
    """
    View: /about/
    """
    return render(request, 'about.html')


def tool(request, name):
    """
    View: /tool/<name>/
    """
    try:
        tool = Tools.objects.get(name=name)
        data = {'tool': tool}
        return render(request, 'tool.html', data)
    except ObjectDoesNotExist:
        message(request, 'warning', 'The tool you were looking for was not found: {}'.format(name))
        return redirect('home:index')
    except Exception as error:
        logger.exception(error)
        message(request, 'danger', 'An unknown error occurred: {}'.format(error))
        return redirect('home:index')


@login_required
def profile(request):
    """
    View: /profile/
    """
    try:
        data = {'ldap': request.user.ldap_user.attrs} if hasattr(request.user, 'ldap_user') else {}
        return render(request, 'profile.html', data)
    except Exception as error:
        logger.exception(error)
        message(request, 'danger', 'An unknown error occurred: {}'.format(error))
        return redirect('home:index')
