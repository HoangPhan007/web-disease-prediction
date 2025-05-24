# from turtle import pd
import pandas as pd

from django.contrib.auth.models import User, AbstractUser

from django.db import models
import json
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group, Permission

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


class userHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết với người dùng đã thực hiện kiểm tra
    test_type = models.CharField(max_length=120)              # Tên loại kiểm tra (PCOS, Mental Disorder, Obesity)
    symptoms = models.CharField(max_length=500)               # Danh sách triệu chứng (dạng chuỗi JSON)
    result = models.CharField(max_length=120)                 # Kết quả dự đoán từ mô hình
    date = models.DateField(default=timezone.now)             # Ngày thực hiện kiểm tra

    def set_symptoms(self, symptoms_list):  # Lưu triệu chứng dưới dạng JSON
        self.symptoms = json.dumps(symptoms_list)

    def get_symptoms(self):                 # Trả lại triệu chứng dưới dạng list
        return json.loads(self.symptoms)



class pcosDisorder(models.Model):
    BLOOD_GROUP_CHOICES = (   # Danh sách nhóm máu
        ('11', 'A+'), ('12', 'A-'), ('13', 'B+'), ('14', 'B-'),
        ('15', 'O+'), ('16', 'O-'), ('17', 'AB+'), ('18', 'AB-'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người thực hiện bài kiểm tra
    period_frequency = models.IntegerField(                   # Tần suất kinh nguyệt trong 1 năm
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    # Các câu hỏi YES/NO (1/0) thể hiện triệu chứng
    gained_weight = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    body_hair_growth = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    skin_dark = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    hair_problem = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    pimples = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    fast_food = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    exercise = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    mood_swing = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))
    mentrual_regularity = models.BooleanField(choices=((1, 'YES'), (0, 'NO')))

    duration = models.IntegerField(                          # Số ngày hành kinh
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    blood_grp = models.CharField(                            # Nhóm máu
        max_length=100, choices=BLOOD_GROUP_CHOICES
    )

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người đặt lịch
    appointment_date = models.DateTimeField()                 # Ngày giờ hẹn gặp bác sĩ


class obesityDisorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Người thực hiện kiểm tra
    activityLevel = models.CharField(                         # Mức độ vận động (1: ít, 4: cao)
        max_length=10,
        choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'))
    )


class DoctorUser(AbstractUser):  # Kế thừa từ User, mở rộng thêm thông tin bác sĩ
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)    # Chuyên ngành
    hospital = models.CharField(max_length=255)          # Bệnh viện công tác
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    about = models.CharField(max_length=1000)            # Giới thiệu bản thân
    education = models.CharField(max_length=1000)        # Trình độ học vấn
    experience = models.CharField(max_length=1000)       # Kinh nghiệm
    languages = models.CharField(max_length=1000)        # Ngôn ngữ có thể nói
    expertise = models.CharField(max_length=1000)        # Lĩnh vực chuyên môn

    class Meta:
        db_table = 'doctor_user'

    # Các quyền giống User
    groups = models.ManyToManyField(Group, related_name='doctor_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='doctor_users', blank=True)

    USERNAME_FIELD = 'username'

class AppointmentData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)         # Người đặt lịch
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE) # Bác sĩ được đặt lịch
    email = models.CharField(max_length=150)                         # Email liên hệ
    phone = models.CharField(max_length=20)                          # Số điện thoại liên hệ
    appointmentDate = models.DateTimeField()                         # Ngày hẹn
    message = models.CharField(max_length=1000)                      # Ghi chú từ người bệnh
    status = models.CharField(max_length=50, default="Pending")      # Trạng thái (Pending, Confirmed, Done)
