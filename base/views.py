from django.contrib.auth import logout, authenticate, login as logon
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token

from base.forms import RegistrationForm
from base.models import Developer
from locations.models import Country, Continent, State
from utils import utility_functions, global_variables
from utils.utility_classes import NirvanaLogger
from django.contrib.sessions.models import Session

logger = NirvanaLogger(__name__)

@csrf_exempt
def contact(request):
    try:
        if request.method == 'POST':
            message = None
            # Method to truncate session table to control the row count limit on Heroku.
            if request.user.is_superuser and 'clear_session' in request.POST:
                Session.objects.all().delete()
                message = "Session cleared!"
            # ---------------------------------------------------------------------->>>>
            else:
                data = request.POST
                location = 'Send via portfolio'
                if 'location' in data:
                    location = data['location']
                message_string = utility_functions.get_email_string(data['name'], data['email'],
                                                                    data['subject'], location,
                                                                    data['message'])
                utility_functions.send_email(strip_tags(message_string))
                message = 'Message sent successfully!'
            return JsonResponse({'data': message})
    except Exception as ex:
        logger.write_to_console(str(ex), 'contact function')
        return JsonResponse({'data': 'Oh oh! Something went wrong!'})


def login(request):
    try:
        message = None
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                logon(request, user)
                return redirect('home')
            else:
                message = 'Failed to authenticate!'
        return render(request, 'login.html', {'message': message, 'title': 'Login'})
    except Exception as ex:
        logger.write_to_console(str(ex), 'login')
        request.session['message'] = str(ex)
        return redirect('error')


def register(request):
    try:
        message = None
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                if password == form.cleaned_data['password2']:
                    if utility_functions.validate_password(password):
                        Developer.objects.create_user(username=username, password=password)
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                            logon(request, user)
                            message = 'success'
                        else:
                            message = 'Failed to authenticate!'
                    else:
                        message = global_variables.PASSWORD_COMPLEXITY
                else:
                    message = 'Passwords do not match!'
            else:
                message = form.errors
        request.session['message'] = message
        return redirect('home')
    except Exception as ex:
        logger.write_to_console(str(ex), 'register')
        request.session['message'] = str(ex)
        return redirect('error')


@login_required
def resetpassword(request):
    try:
        message = None
        set = None
        if not request.user.has_usable_password():
            set = True
        if request.method == 'POST':
            user = request.user
            if set:
                user.set_password(request.POST['password'])
                user.save()
                return redirect('home')
            else:
                curr_password = request.POST['curr_password']
                user = authenticate(request, username=user.username, password=curr_password)
                if user is not None:
                    user.set_password(request.POST['password'])
                    user.save()
                    return redirect('home')
                message = 'Failed to authenticate!'
        return render(request, 'resetpassword.html', {'set': set, 'message': message, 'title': 'Reset password'})
    except Exception as ex:
        logger.write_to_console(str(ex), 'reset password')
        request.session['message'] = str(ex)
        return redirect('error')


def home(request):
    try:
        data = {
            'title': 'Home',
            'countries_len': len(Country.objects.all()),
            'continents_len': len(Continent.objects.all()),
            'states_len': len(State.objects.all()),
        }
        return render(request, 'home.html', data)
    except Exception as ex:
        logger.write_to_console(str(ex), 'Home page')
        request.session['message'] = str(ex)
        return redirect('error')


@login_required
def token(request):
    try:
        key, flag = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': key.key})
    except Exception as ex:
        logger.write_to_console(str(ex), 'fetch token')
        request.session['message'] = str(ex)
        return None


@login_required
def logoff(request):
    try:
        logout(request)
        return redirect('home')
    except Exception as ex:
        logger.write_to_console(str(ex), 'logout')
        request.session['message'] = str(ex)
        return redirect('error')
