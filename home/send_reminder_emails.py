# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from home.models import MedicineReminder
# from .email_utils import send_medicine_reminder_email

# class Command(BaseCommand):
#     help = 'Send medicine reminder emails to users based on current time'

#     def handle(self, *args, **kwargs):
#         now = timezone.now()
#         current_time = now.time().replace(second=0, microsecond=0)
#         today = now.date()

#         reminders = MedicineReminder.objects.filter(
#             start_date__lte=today,
#             end_date__gte=today,
#             time_of_day=current_time
#         )

#         if not reminders.exists():
#             self.stdout.write("No reminders to send at this time.")
#             return

#         for reminder in reminders:
#             user_email = reminder.user.email
#             if not user_email:
#                 self.stdout.write(f"User {reminder.user.username} không có email.")
#                 continue

#             send_medicine_reminder_email(
#             email=request.user.email,
#             medicine_name=reminder.medicine_name,
#             dosage=reminder.dosage,
#             usage_instructions=reminder.usage_instructions,
#             start_date=reminder.start_date,
#             end_date=reminder.end_date,
#             time_of_day=reminder.time_of_day,
#             frequency_per_day=reminder.frequency_per_day,
#             additional_notes=reminder.additional_notes
#         )

#             self.stdout.write(f"Đã gửi email cho {reminder.user.username} - {user_email}")
from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import MedicineReminder
from .email_utils import send_medicine_reminder_email
import pytz
from datetime import datetime, timedelta
from django.conf import settings

class Command(BaseCommand):
    help = 'Send medicine reminder emails to users based on current time'

    def handle(self, *args, **kwargs):
        local_tz = pytz.timezone('Asia/Ho_Chi_Minh')  # chỉnh múi giờ VN
        now = timezone.now().astimezone(local_tz)
        today = now.date()
        current_time = now.time().replace(second=0, microsecond=0)

        one_minute_later = (datetime.combine(today, current_time) + timedelta(minutes=1)).time()

        reminders = MedicineReminder.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
            time_of_day__gte=current_time,
            time_of_day__lt=one_minute_later,
        )

        if not reminders.exists():
            self.stdout.write("No reminders to send at this time.")
            return

        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')

        for reminder in reminders:
            user_email = reminder.user.email
            if not user_email:
                self.stdout.write(f"User {reminder.user.username} không có email.")
                continue

            try:
                send_medicine_reminder_email(reminder, base_url=base_url)
                self.stdout.write(f"Đã gửi email cho {reminder.user.username} - {user_email}")
            except Exception as e:
                self.stderr.write(f"Lỗi khi gửi email cho {reminder.user.username}: {e}")
