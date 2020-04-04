from django import forms
from .models import CustomUser
from .models import Commorbidity
from .models import Symptom
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _



class CustomSignUpForm(forms.ModelForm):
    # age = forms.IntegerField(min_value=0)
    # gender = forms.ChoiceField(choices=CustomUser.Gender.choices)
    # household_size = forms.IntegerField(min_value=0)
    # commorbidities = forms.ModelMultipleChoiceField(queryset=Commorbidity.objects.all())
    # symptoms = forms.ModelMultipleChoiceField(queryset=Symptom.objects.all())

    # username = forms.CharField(max_length=200)
    # email = forms.EmailField()
    # password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['age', 'gender', 'household_size', 'commorbidities', 'symptoms']


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
