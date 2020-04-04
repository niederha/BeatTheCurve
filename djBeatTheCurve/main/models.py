from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Commorbidity(models.Model):
    name = models.CharField(max_length=200)

class CustomUser(models.Model):

    class Gender(models.TextChoices):
        FEMALE = 'F', _('Female')
        MALE = 'M', _('Male')
        OTHER = 'O', _('Other')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    household_size = models.PositiveIntegerField()
    commorbidities = models.ForeignKey(Commorbidity, on_delete=models.DO_NOTHING)

class GameInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_leave = models.DateTimeField('last household leave')
    last_hand_wash = models.DateTimeField('last hand wash')
    last_physical_activity = models.DateTimeField('last physical activity')
    score = models.IntegerField()