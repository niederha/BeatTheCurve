from django.contrib import admin

from .models import Commorbidity
from .models import Symptom
from .models import CustomUser

# Register your models here.

admin.site.register(Commorbidity)
admin.site.register(Symptom)
admin.site.register(CustomUser)