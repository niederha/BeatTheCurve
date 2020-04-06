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

from datetime import datetime, timedelta
from dateutil import tz

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
    top_cusers = top_cusers[:top_size]
    #test_users = CustomUser.objects.filter(symptoms__name__in=[Symptom.SymptomType.COUGH, Symptom.SymptomType.FEVER])
    #print(test_users)

    return render(request, 'main/dashboard_final.html', {'saved':123, 'score':cuser.score, 'top_cusers':top_cusers})


def daily(request):
    def save_log(user, form):
        log_entry = form.save(commit=False)
        log_entry.user = user # Set log entry to current user
        log_entry.date = datetime.now(tz.gettz(settings.TIME_ZONE))
        log_entry.save()
        form.save_m2m()

    def update_score(user, form):
        game_info = GameInfo.objects.get(user=user)
        if form.cleaned_data['leave'] == 'n':
            game_info.score += 10
        else:
            if form.cleaned_data['hand_wash_after_leave'] == 'y':
                game_info.score += 5
            
            reasons = list(form.cleaned_data['reason'])
            for reason in reasons:
                if not reason.is_sensible():
                    game_info.score += reason.get_score()
                

        game_info.save()
        
    # TODO: Should check if user is doing modifications, or if it is the first daily submission today
    # to compute score correctly. To ease the process, the score of a submission should be added to the daily model.
    # This way, a modification can easily first subtract the score that was added, and then add the modified one that
    # has been updated.

    if request.method == 'POST':
        form = LogEntryForm(request.POST)

        if form.is_valid():
            print("LogEntry form is valid")
            save_log(request.user, form)
            update_score(request.user, form)

            print("Successfully save log entry, redirecting to dashboard")
            return HttpResponseRedirect('dashboard')
        else:
            print("LogEntry form is NOT valid")
            return HttpResponseRedirect('daily')
    
    else:
        return render(request, 'main/daily.html', {'form': LogEntryForm()})


def simulation(request):
    def crowded_places_frequentation_mean(user):
        user_logs = LogEntry.objects.filter(log_user=user)
        user_logs = user_logs.annotate(
            crowded_outing=Case(
                When(crowded_places='y', then=Value(1)),
                default=Value(0),
                output_field=IntegerField
            ),
        ).values_list('log_user', 'date', 'crowded_outing')
        user_logs_list = list(user_logs)

        # Ugly but will suffice as proof of concept as sqlite does not implement moving average and coding it in django is awful..
        
        # Problem: Rolling average over missing daily logs that a replaced with the value 0 does not give the right statistic
        # But simply taking the average of available entry logs does not give the right statistic either
        logs_df = pd.DataFrame(data=user_logs_list, columns=('user', 'date', 'out'))
        logs_df['date'] = pd.to_datetime(logs_df['date'])
        logs_df = logs_df.set_index('date')

        full_date_range = pd.date_range(logs_df.index.min(), logs_df.index.max(), freq='d')

        full_date_range_df = pd.DataFrame(full_date_range, columns=('date',))
        full_date_range_df = full_date_range_df.set_index('date')

        joined_df = logs_df.join(full_date_range_df, how='outer')
        joined_df = joined_df.fillna(0)

        result = joined_df['out'].rolling('7d').mean()

        return result.mean()

    def get_hand_hygiene_mean(user):
         # Problem: Rolling average over missing daily logs that a replaced with the value 0 does not give the right statistic
        # But simply taking the average of available entry logs does not give the right statistic either
        def get_sim_param_from_score(score):
            switch = {
                0: 0.5,
                1: 1,
                2: 1.5,
                3: 2,
            }
            return switch[score]

        user_logs = LogEntry.objects.filter(log_user=user)
        hand_wash_frequency_avg = user_logs.annotate(
            hand_hygiene=Case(
                When(hand_wash_frequency=LogEntry.HandWashRanges.DIRTY, then=Value(0)),
                When(hand_wash_frequency=LogEntry.HandWashRanges.LOW, then=Value(1)),
                When(hand_wash_frequency=LogEntry.HandWashRanges.HIGH, then=Value(3)),
                default=Value(2),
                output_field=IntegerField
            ),
        ).AVG('hand_hygiene')

        return get_sim_param_from_score(round(hand_wash_frequency_avg))

    def get_leave_frequency(user):
        user_logs = LogEntry.objects.filter(log_user=user)
        
        return user_logs.annotate(
            has_left=Case(
                When(leave='y', then=Value(1)),
                default=Value(0),
                output_field=IntegerField
            ),
        ).AVG('has_left')

    # TODO: Define method to get back mean of hand wash after leave (only if leave was true)
    # THOSE FUNCTiONS SHOULD PROBABLY BE ACCESSIBLE TO DAILIES TO UPDATE THE SCORE
    


        
        



