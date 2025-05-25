# from django.urls import reverse
# from django.core.mail import send_mail
# from django.conf import settings
# from django.urls import reverse
# from django.utils.html import strip_tags

# def send_medicine_reminder_email(request, reminder):
#     from django.utils.html import strip_tags

#     subject = f"Nhắc nhở uống thuốc: {reminder.medicine_name}"

#     # Tạo đường dẫn đầy đủ tới link đánh dấu đã uống
#     mark_done_url = request.build_absolute_uri(
#         reverse('mark_as_done', args=[reminder.id])
#     )

#     message_html = f"""
#     <p>Chào bạn,</p>
#     <p>Đây là lời nhắc sử dụng thuốc của bạn:</p>
#     <ul>
#         <li><strong>Tên thuốc:</strong> {reminder.medicine_name}</li>
#         <li><strong>Liều lượng:</strong> {reminder.dosage}</li>
#         <li><strong>Hướng dẫn sử dụng:</strong> {reminder.usage_instructions}</li>
#         <li><strong>Bắt đầu từ:</strong> {reminder.start_date.strftime('%d/%m/%Y')}</li>
#         <li><strong>Kết thúc vào:</strong> {reminder.end_date.strftime('%d/%m/%Y')}</li>
#         <li><strong>Giờ uống thuốc mỗi ngày:</strong> {reminder.time_of_day.strftime('%H:%M')}</li>
#         <li><strong>Số lần uống mỗi ngày:</strong> {reminder.frequency_per_day}</li>
#     </ul>
#     <p><strong>Ghi chú thêm:</strong> {reminder.additional_notes or '-'}</p>
#     <p>
#         👉 <a href="{mark_done_url}">Nhấn vào đây để đánh dấu là đã uống</a>
#     </p>
#     <p>Chúc bạn mau khỏe!</p>
#     """

#     send_mail(
#         subject,
#         strip_tags(message_html),  # nội dung text fallback
#         settings.DEFAULT_FROM_EMAIL,
#         [reminder.user.email],
#         html_message=message_html,
#         fail_silently=False,
#     )
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags

def send_medicine_reminder_email(reminder, base_url=None):
    if not base_url:
        raise ValueError("base_url is required to build absolute URLs")

    mark_done_url = f"{base_url}{reverse('mark_as_done', args=[reminder.id])}"

    subject = f"Nhắc nhở uống thuốc: {reminder.medicine_name}"

    message_html = f"""
    <p>Hello,</p>
    <p>This is your medication reminder:</p>
    <ul>
        <li><strong>Medicine name:</strong> {reminder.medicine_name}</li>
        <li><strong>Dosage:</strong> {reminder.dosage}</li>
        <li><strong>Usage instructions:</strong> {reminder.usage_instructions}</li>
        <li><strong>Start date:</strong> {reminder.start_date.strftime('%d/%m/%Y')}</li>
        <li><strong>End date:</strong> {reminder.end_date.strftime('%d/%m/%Y')}</li>
        <li><strong>Time to take medicine each day:</strong> {reminder.time_of_day.strftime('%H:%M')}</li>
        <li><strong>Frequency per day:</strong> {reminder.frequency_per_day}</li>
    </ul>
    <p><strong>Additional notes:</strong> {reminder.additional_notes or '-'}</p>
    <p>
        👉 <a href="{mark_done_url}">Click here to mark as taken</a>
    </p>
    <p>Wishing you a speedy recovery!</p>
    """
    send_mail(
        subject,
        strip_tags(message_html),  # plain text fallback
        settings.DEFAULT_FROM_EMAIL,
        [reminder.user.email],
        html_message=message_html,
        fail_silently=False,
    )
