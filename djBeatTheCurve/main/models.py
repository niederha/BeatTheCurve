from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Commorbidity(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"""Commorbidity [
            Name: {self.name}
        ]
        """

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
    household_size = models.PositiveIntegerField(default=1)
    commorbidities = models.ManyToManyField(Commorbidity)

    def __str__(self):
        return f"""CustomUser [
            Username: {self.user!s},
            Age: {self.age},
            Gender: {self.gender},
            Household size: {self.household_size},
            Commorbidities: {self.commorbidities}
        ]
        """

class GameInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_leave = models.DateTimeField('last household leave')
    last_hand_wash = models.DateTimeField('last hand wash')
    last_physical_activity = models.DateTimeField('last physical activity')
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"""GameInfo [
            Username: {self.user!s},
            Date of last household leave: {self.last_leave},
            Date of last hand wash: {self.last_hand_wash},
            Date of last physical activity: {self.last_physical_activity},
            Score: {self.score}
        ]
        """