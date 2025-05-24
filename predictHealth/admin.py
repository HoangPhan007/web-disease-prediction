from django.contrib import admin
from home.models import (
    Appointment, AppointmentData,
    obesityDisorder, pcosDisorder,
    UserProfile, mentalDisorder,
    MedicineReminder
)

admin.site.register(Appointment)
admin.site.register(AppointmentData)
admin.site.register(obesityDisorder)
admin.site.register(pcosDisorder)
admin.site.register(UserProfile)
admin.site.register(mentalDisorder)
admin.site.register(MedicineReminder)
