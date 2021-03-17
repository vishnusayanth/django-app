import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from base.forms import RegistrationForm
from base.models import RequestCounter
from utils import global_variables
from utils.utility_classes import NirvanaLogger

logger = NirvanaLogger(__name__)


def cleanup_social_account(backend, uid, user=None, *args, **kwargs):
    try:
        if user and kwargs.get('is_new', False):
            user.username = kwargs['details']['username']
            if 'html_url' in kwargs['response']:
                user.url = kwargs['response']['html_url']
            else:
                user.url = global_variables.LINKEDIN_URL + str(user.username).replace(' ', '-')
            user.save()
    except Exception as ex:
        logger.write_to_console(str(ex), ' clean up after social login.')
    return {'user': user}


def custom_context(request):
    return {
        'zomato_url': global_variables.ZOMATO_IFRAME_URL,
        'locations': global_variables.GET_STATES,
        'continents': global_variables.GET_CONTINENTS,
        'registrationform': RegistrationForm()
    }


def CustomRequestMiddleware(get_response):
    # Below function serves the purpose of testing a custom middleware.
    # This function keeps track of number of requests processed by this application and clears
    def middleware(request):
        # if the message is passed to the template once, remove the message from the next request.
        # this message is used mainly for error messages.
        if 'message_shown' in request.session and 'message' in request.session:
            if request.session['message_shown']:
                request.session['message'] = None
                request.session['message_shown'] = False
            elif request.session['message'] is not None:
                request.session['message_shown'] = True
        else:
            request.session['message'] = None
            request.session['message_shown'] = False

        obj = RequestCounter.objects.first()
        if obj is None:
            obj = RequestCounter.objects.create(count=0)
        obj.count += 1
        obj.save()
        response = get_response(request)
        return response

    return middleware


def get_email_string(name, email, subject, location, message):
    return '''
Hey there! <br/>
{name} has sent you a message.<br/><br/>
Email : {email},  <br/>
Subject : {subject},  <br/>
Location : {location},  <br/><br/>
This is the message,
<br/>
'''.format(name=name, email=email, subject=subject, location=location) + message


def send_email(message_string):
    try:
        message_string = global_variables.email_frame.replace('{0}', message_string)
        s = smtplib.SMTP(host=global_variables.SMTP_SERVER, port=587)
        s.starttls()
        s.login(global_variables.EMAIL, global_variables.EMAIL_PASSWORD)
        msg = MIMEMultipart()
        msg['From'] = global_variables.EMAIL
        msg['To'] = 'vishnusayanth@gmail.com'
        msg['Subject'] = "Message from NIRVANA app"
        msg.attach(MIMEText(message_string, 'html'))
        s.send_message(msg)
        del msg
        s.quit()
    except Exception as ex:
        logger.write_to_console(str(ex), ' send email.')


def validate_password(password):
    if len(password) >= 7 and any(char.isdigit() for char in password) and any(
            char.isalpha() for char in str(password)):
        return True
