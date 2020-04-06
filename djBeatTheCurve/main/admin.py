from django.contrib import admin

from .models import Commorbidity
from .models import Symptom
from .models import CustomUser
from .models import GameInfo
from .models import OutingReason

# Register your models here.

admin.site.register(Commorbidity)
admin.site.register(Symptom)
admin.site.register(CustomUser)
admin.site.register(GameInfo)
admin.site.register(OutingReason)