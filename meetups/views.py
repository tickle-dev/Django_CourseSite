from meetups.forms import RegistrationForm
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Meetup, Participant

def index(request):
    meetups = Meetup.objects.all()

    return render(request, 'meetups/index.html', {
        'meetups' : meetups
    })

def metup_details(request, meetup_slug):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        if request.method == 'GET':
            registration_form = RegistrationForm()
        else:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data['email']
                participant, _ = Participant.objects.get_or_create(email=user_email)
                selected_meetup.participants.add(participant)
                return redirect('confirm-registration', meetup_slug=meetup_slug)

        return render(request, 'meetups/meetup-details.html', {
        'meetup_found' : True,
        'meetup' : selected_meetup,
        'form' : registration_form
    })
    except Exception as exc:
        return render(request, 'meetups/meetup-details.html', {
            'meetup_found' : False
        })

def confirm_registration(request, meetup_slug):
    meetup = Meetup.objects.get(slug=meetup_slug)
    return render(request, 'meetups/registrations.html', {
        'org_email' : meetup.org_email
    })   
