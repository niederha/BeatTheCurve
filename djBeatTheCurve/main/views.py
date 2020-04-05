from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.http import QueryDict
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.conf import settings

from django.db.models import Case, When, Value, Window, F, Avg, Min, ValueRange, IntegerField
from .models import CustomUser, GameInfo, LogEntry
from .models import Symptom


from .forms import CustomSignUpForm, EasyUserCreationForm, LogEntryForm

from datetime import datetime

import pandas as pd

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

def customSignUp(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)

        if form.is_valid():
            print("Customuser form is valid")
            custom_user = form.save(commit=False)
            custom_user.user = request.user # Set custom user to current user
            print(request.user)
            custom_user.save()
            form.save_m2m()

            game_info = GameInfo(user=request.user)
            game_info.save()

            print("Successfully save custom user, redirecting to dashboard")
            return HttpResponseRedirect('dashboard')
        else:
            return HttpResponseRedirect('customsignup')
    
    else:
        form = CustomSignUpForm()
        return render(request, 'main/custom_sign_up_final.html', {'form': form})

def signUp(request):
    if request.method == 'POST':
        user_form = EasyUserCreationForm(request.POST)

        print(user_form)
        if user_form.is_valid():
            print("User successfully created")
            user_form.save()

            return HttpResponseRedirect('signin')
        else:
            print("FAILED to create user")
            return render(request, 'main/sign_up_final.html', {'form': EasyUserCreationForm()})
    else:
        user_form = EasyUserCreationForm()

        return render(request, 'main/sign_up_final.html', {'form': user_form})

def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("LOGGED IN")
            if CustomUser.objects.all().filter(user=user).exists():
                return HttpResponseRedirect('dashboard')
            else:
                return HttpResponseRedirect('customsignup')
        else:
            print("FAILED TO LOG IN")
            return HttpResponseRedirect('signin')
    else:
        return render(request, 'main/sign_in_final.html', {'form': AuthenticationForm()})

def dashboard(request):
    print("HELLO FROM DASHBOARD")

    cuser = GameInfo.objects.get(user=request.user)
    top_cusers = GameInfo.objects.order_by('-score')
    top_size = min(top_cusers.count(), 4)
    top_cusers = top_cusers[:4]
    #test_users = CustomUser.objects.filter(symptoms__name__in=[Symptom.SymptomType.COUGH, Symptom.SymptomType.FEVER])
    #print(test_users)

    return render(request, 'main/dashboard_final.html', {'saved':123, 'score':cuser.score, 'top_cusers':top_cusers})


def daily(request):
    if request.method == 'POST':
        form = LogEntryForm(request.POST)

        if form.is_valid():
            print("LogEntry form is valid")
            log_entry = form.save(commit=False)
            log_entry.user = request.user # Set log entry to current user
            log_entry.date = datetime.now(settings.TIME_ZONE)
            log_entry.save()
            form.save_m2m()

            print("Successfully save log entry, redirecting to dashboard")
            return HttpResponseRedirect('dashboard')
        else:
            return HttpResponseRedirect('daily')
    
    else:
        return render(request, 'main/daily_test.html', {'form': LogEntryForm()})


def simulation(request):
    def crowded_places_frequentation_mean(user):
        user_logs = LogEntry.objects.filter(log_user=user)
        min_log_date = user_logs.aggregate(Min('date'))
        user_logs = user_logs.annotate(
            crowded_outing=Case(
                When(crowded_places='y', then=Value(1)),
                default=Value(0),
                output_field=IntegerField
            ),
        ).values_list('log_user', 'date', 'crowded_outing')
        user_logs_list = list(user_logs)

        # Ugly but will do as sqlite does not implement moving average and coding it in django is awful..
        
        



