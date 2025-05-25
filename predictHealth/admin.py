from django.contrib import admin

from home.models import (
    Appointment,Appointment_1, AppointmentData,
    obesityDisorder, pcosDisorder,
    UserProfile, mentalDisorder,
    MedicineReminder,Doctor_1, DoctorSchedule,
)

admin.site.register(Appointment)
admin.site.register(AppointmentData)
admin.site.register(obesityDisorder)
admin.site.register(pcosDisorder)
admin.site.register(UserProfile)
admin.site.register(mentalDisorder) 
admin.site.register(MedicineReminder)

admin.site.register(Appointment_1)
admin.site.register(Doctor_1)
admin.site.register(DoctorSchedule)