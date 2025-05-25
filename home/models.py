# from turtle import pd
import pandas as pd
from django.utils import timezone
import json
from django.contrib.auth.models import User

from django.db import models

from django.db import models
from django.contrib.auth.models import User
class userHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_type = models.CharField(max_length = 120)
    symptoms = models.CharField(max_length = 500)
    result = models.CharField(max_length = 120)
    date = models.DateField(default=timezone.now)

    def set_symptoms(self, symptoms_list):
        self.symptoms = json.dumps(symptoms_list)

    def get_symptoms(self):
        return json.loads(self.symptoms)

from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.appointment_date}"
from django.db import models
from django.contrib.auth.models import User

class AppointmentData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.appointment_date}"
from django.db import models
from django.contrib.auth.models import User

class obesityDisorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bmi = models.FloatField()
    diagnosis_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - BMI: {self.bmi}"
class pcosDisorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diagnosis_date = models.DateField(null=True, blank=True)
    symptoms = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - PCOS Disorder"

# chuẩn bị dataset cho model
mental_disorder_df = pd.read_csv('static/mentalDisorder.csv')

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)

    @property
    def bmi(self):
        if self.height and self.weight:
            return round(self.weight / ((self.height / 100) ** 2), 2)
        return None

# định nghãi entity, model cho đối tượng dự đoán sức khỏe tâm thần.
class mentalDisorder(models.Model):
    choices_dict = {}
    for column in mental_disorder_df.columns:
        unique_values = mental_disorder_df[column].unique()
        choices = [(val, val) for val in unique_values]
        choices_dict[column] = choices

    # Liên kết mỗi bản ghi với một người dùng cụ thể trong hệ thống (bảng User của Django)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Mức độ cảm thấy buồn bã, mất hứng thú trong cuộc sống hàng ngày
    sadness = models.CharField(max_length=100, choices=choices_dict['Sadness'])

    # Cảm xúc hưng phấn bất thường (cảm thấy cực kỳ vui vẻ, năng lượng cao bất thường)
    euphoric = models.CharField(max_length=100, choices=choices_dict['Euphoric'])

    # Cảm thấy kiệt sức cả về thể chất và tinh thần
    exhausted = models.CharField(max_length=100, choices=choices_dict['Exhausted'])

    # Rối loạn giấc ngủ (mất ngủ, ngủ nhiều, ngủ không sâu)
    sleep_disorder = models.CharField(max_length=100, choices=choices_dict['Sleep dissorder'])

    # Thay đổi cảm xúc đột ngột, dễ cáu gắt hoặc buồn vui thất thường
    mood_swing = models.CharField(max_length=100, choices=choices_dict['Mood Swing'])

    # Suy nghĩ về việc tự tử hoặc làm tổn thương bản thân
    suicidal_thoughts = models.CharField(max_length=100, choices=choices_dict['Suicidal thoughts'])

    # Biếng ăn, chán ăn hoặc ăn rất ít
    anorxia = models.CharField(max_length=100, choices=choices_dict['Anorxia'])  # Lưu ý: nên đổi thành 'anorexia'

    # Mức độ tôn trọng người có thẩm quyền hoặc tuân thủ quy tắc
    authority_respect = models.CharField(max_length=100, choices=choices_dict['Authority Respect'])

    # Phản ứng khi bị hiểu lầm hoặc chỉ trích – có cố gắng giải thích không
    try_explanation = models.CharField(max_length=100, choices=choices_dict['Try-Explanation'])

    # Phản ứng một cách hung hăng khi bị phản bác hoặc gặp áp lực
    aggressive_response = models.CharField(max_length=100, choices=choices_dict['Aggressive Response'])

    # Có xu hướng bỏ qua mọi việc và tiếp tục tiến về phía trước
    ignore_moveon = models.CharField(max_length=100, choices=choices_dict['Ignore & Move-On'])

    # Đã từng trải qua suy sụp tinh thần nghiêm trọng, mất kiểm soát cảm xúc
    nervous_breakdown = models.CharField(max_length=100, choices=choices_dict['Nervous Break-down'])

    # Mức độ sẵn sàng thừa nhận lỗi lầm khi mắc sai sót
    admit_mistakes = models.CharField(max_length=100, choices=choices_dict['Admit Mistakes'])

    # Có thường xuyên suy nghĩ quá mức, lo xa, hoặc suy nghĩ tiêu cực không
    overthink = models.CharField(max_length=100, choices=choices_dict['Overthinking'])

    # Mức độ hoạt động tình dục, có biểu hiện bất thường hoặc bị ảnh hưởng bởi tinh thần không
    sexual_activity = models.CharField(max_length=100, choices=choices_dict['Sexual Activity'])

    # Khả năng tập trung vào công việc, học tập – có bị phân tâm nhiều không
    concentration = models.CharField(max_length=100, choices=choices_dict['Concentration'])

    # Mức độ lạc quan trong suy nghĩ, có nhìn nhận tích cực về cuộc sống không
    optimisim = models.CharField(max_length=100, choices=choices_dict['Optimisim'])  # Lưu ý: nên đổi thành 'optimism'
# Danh models.py
class MedicineReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    usage_instructions = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    time_of_day = models.TimeField()
    frequency_per_day = models.IntegerField(default=1)
    additional_notes = models.TextField(blank=True, null=True)
    reminder_method = models.CharField(
        max_length=100,
        choices=[('email', 'Email')],
        default='email'
    )

    STATUS_CHOICES = [
        ('pending', 'Chưa hoàn thành'),
        ('done', 'Đã uống'),
        ('completed', 'Hoàn thành'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')



    def __str__(self):
        return f"{self.user.username} - {self.medicine_name}"
class ReminderTime(models.Model):
    reminder = models.ForeignKey(MedicineReminder, on_delete=models.CASCADE)