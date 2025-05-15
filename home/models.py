# from turtle import pd
import pandas as pd

from django.contrib.auth.models import User

from django.db import models

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
