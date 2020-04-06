from django import forms
from .models import CustomUser, Commorbidity, Symptom, LogEntry
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class EasyUserCreationForm(UserCreationForm):
    def _post_clean(self):
        super(UserCreationForm, self)._post_clean()

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
        widgets = {'gender': forms.RadioSelect, 'commorbidities': forms.CheckboxSelectMultiple, 'symptoms': forms.CheckboxSelectMultiple}

class LogEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        exclude = ['user', 'date']
        widgets = {'hand_wash_frequency': forms.RadioSelect, 'leave': forms.RadioSelect, 'crowded_places': forms.RadioSelect, 
                    'hand_wash_after_leave': forms.RadioSelect, 'reason': forms.CheckboxSelectMultiple}

class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()


