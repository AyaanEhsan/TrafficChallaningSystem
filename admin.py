from django.contrib import admin
from .models import ComplaintModel, RegistrationModel
# Register your models here.
admin.site.register(ComplaintModel)
admin.site.register(RegistrationModel)