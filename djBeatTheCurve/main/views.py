from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.http import QueryDict
from django.http import HttpResponseRedirect
from django.contrib.auth.models import UserManager
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

from .models import CustomUser
from .models import Symptom

from .forms import CustomSignUpForm

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
            custom_user.save()

            print("Successfully save custom user, redirecting to dashboard")
            return HttpResponseRedirect('dashboard')
        else:
            return HttpResponseRedirect('customsignup')
    
    else:
        form = CustomSignUpForm()
        return render(request, 'main/custom_sign_up_final.html', {'form': form})

def signUp(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        print(user_form)
        if user_form.is_valid():
            print("User successfully created")
            user_form.save()

            return HttpResponseRedirect('customsignup')
        else:
            print("FAILED to create user")
            return render(request, 'main/sign_up_final.html', {'form': UserCreationForm()})
    else:
        user_form = UserCreationForm()

        return render(request, 'main/sign_up_final.html', {'form': user_form})

def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            HttpResponseRedirect('dashboard')
            print("LOGGED IN")
        else:
            print("FAILED TO LOG IN")
            HttpResponseRedirect('signin')
    else:
        return render(request, 'main/signin.html', {'form': AuthenticationForm()})

def dashboard(request):
    print("HELLO FROM DASHBOARD")




# def signIn(request):
#     if request.method == 'POST':
#         user_form = UserCreationForm(request.POST)

#         if user_form.is_valid():
#             user_form.save()

#         return HttpResponseRedirect('')
#     else:
#         user_form = UserCreationForm()

#         return render(request, 'main/signup.html', {'form': user_form})


# def signUp(request):
    
#     if request.method == 'POST':
#         print("HELLO GUYS")
#         print(request.POST)

#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']

#         UserManager.create_user(username, password=password, email=email)
#         user.set_password(password)
#         custom_user_form = SignUpForm(request.POST or None)
        
#         if custom_user_form.is_valid():
#             print("EVERYTHING IS VALID")

#             custom_user = custom_user_form.save(commit='False')
#             custom_user.user = user
#             custom_user.save()

#             return HttpResponseRedirect('') # TODO

#         print(f"Some form in invalid: custom_user_form:{custom_user_form.is_valid()} ")
#     else:
#         custom_user_form = SignUpForm()

#     return render(request, 'main/signup.html', {'custom_user_form': custom_user_form})