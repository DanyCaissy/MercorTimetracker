from django.http import HttpResponse

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from .tokens import account_activation_token
from .forms import SetPasswordForm  # ✅ Import the password form
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Index Page")

def send_activation_email(user, request):
    """ Send activation email to the new user """
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    activation_link = f"http://{domain}/activate/{uid}/{token}/"

    mail_subject = "Activate your account"
    message = render_to_string('Timetracker/activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })

    try:
        send_mail(mail_subject, message, 'noreply@example.com', [user.email])
        print("Email sent successfully!")
    except Exception as e:
        print("Email failed:", e)

def activate(request, uidb64, token):
    """ Activate user and allow them to set a password """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data["password1"])  #  Set new password
                user.is_active = True  #  Activate user
                user.save()
                login(request, user)  #  Log in user after setting password
                return redirect("dashboard")  #  Redirect to dashboard after activation
        else:
            form = SetPasswordForm()

        return render(
            request,
            "Timetracker/activation_form.html",
            {"form": form, "user": user},
        )
    else:
        return HttpResponse("Activation was not successful.")

@login_required  #  Ensures only logged-in users can access this page
def dashboard(request):
    software_download_url = "www.google.com"

    return render(request, "Timetracker/dashboard.html", {
        "user": request.user,
        "software_download_url": software_download_url,
    })