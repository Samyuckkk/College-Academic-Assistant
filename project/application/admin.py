from django.contrib import admin
from application.models import Appointment, AcceptedAppointment, Subject

# Register your models here.

admin.site.register(Appointment)
# admin page login pass same -> superuser

admin.site.register(AcceptedAppointment)


admin.site.register(Subject)