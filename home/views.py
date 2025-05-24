from urllib import request

import joblib
import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from pyexpat.errors import messages

from django.shortcuts import render, redirect
from django import forms
from .models import UserProfile, mentalDisorder

mental_disorder_model = joblib.load('static/models/mental_disorder_prediction.pkl')
mental_disorder_encoder = joblib.load('static/encoders/mental_disorder_encoder.pkl')
mental_disorder_output_encoder = joblib.load('static/encoders/mental_disorder_output_encoder.pkl')


# form Register information user
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for CSS Properties
        self.fields['username'].widget.attrs.update({'class': 'col-md-10 form-control'})
        self.fields['email'].widget.attrs.update({'class': 'col-md-10 form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'col-md-10 form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'col-md-10 form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'col-md-10 form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'col-md-10 form-control'})

        self.fields['username'].help_text = '<span class="text-muted">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'
        self.fields['email'].help_text = '<span class="text-muted">Required. Inform a valid email address.</span>'
        self.fields['password2'].help_text = '<span class="text-muted">Enter the same password as before, for verification.</span>'
        self.fields['password1'].help_text = '<span class="text-muted"><ul class="small"><li class="text-muted">Your password can not be too similar to your other personal information.</li><li class="text-muted">Your password must contain at least 8 characters.</li><li class="text-muted">Your password can not be a commonly used password.</li><li class="text-muted">Your password can not be entirely numeric.</li></ul></span>'


# Định nghĩa form trong django dựa trên model của mentalDisorder
class MentalDisorderForm(forms.ModelForm):
    class Meta:
        model = mentalDisorder  # liên kết với model mentalDisorder
        fields = '__all__'
        exclude = ['user']

    # Khởi tạo form và tùy biến giao diện
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-md-12'})
            if isinstance(field.widget, forms.Select):
                field.empty_label = "Choose one"


# display home page
def index(request):
    return render(request, 'index.html')

# function register call form Register
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        try:
            if form.is_valid():
                form.save()
                return redirect('login')
        except:
            form = UserRegistrationForm()
            messages.error(request, "Something went wrong. Try again!")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Do not user. Try again!")
    return render(request, 'login.html')



@login_required
def complete_profile(request):
    # if profile exists -> return to dashboard profile page
    if UserProfile.objects.filter(user=request.user).exists():
        return redirect('dashboard')

    if request.method == "POST":
        user_profile = UserProfile.objects.create(
            user=request.user,
            dob=request.POST['dob'],
            gender=request.POST['gender'],
            height=request.POST['height'],
            weight=request.POST['weight'],
            profession=request.POST['profession']
        )
        return redirect('dashboard')

    return render(request, 'profile.html', {'user_name': request.user.first_name + " " + request.user.last_name})


# Hàm hiểm thị dashBoard user, có sử dụng tên user
@login_required
def user_dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'user_dashboard.html',
                  {'user_name': request.user.first_name + " " + request.user.last_name,
                                                'user_profile': user_profile,
                                                'user_username': request.user.username
                                                })


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Phương thức xử lý việc dự đoán rối loạn tâm lý dựa trên dữ liệu người dùng nhập
@login_required  # Đảm bảo chỉ người dùng đã đăng nhập mới truy cập được
def mental_disorder(request):
    if request.method == 'POST':
        # 4.1.3.5 Django Web App tiếp nhận dữ liệu từ biểu mẫu (POST request) và khởi tạo MentalDisorderForm(request.POST)
        form = MentalDisorderForm(request.POST)

        # 4.1.3.6  MentalDisorderForm kiểm tra tính hợp lệ.
        if form.is_valid():
            # Retrieve user-entered data from the form

            # Mức độ cảm thấy buồn bã, mất hứng thú trong cuộc sống hàng ngày
            sadness = form.cleaned_data['sadness']

            # Cảm xúc hưng phấn bất thường (cảm thấy cực kỳ vui vẻ, năng lượng cao bất thường)
            euphoric = form.cleaned_data['euphoric']

            # Cảm thấy kiệt sức cả về thể chất và tinh thần
            exhausted = form.cleaned_data['exhausted']

            # Rối loạn giấc ngủ (mất ngủ, ngủ nhiều, ngủ không sâu)
            sleep_disorder = form.cleaned_data['sleep_disorder']

            # Cảm xúc thay đổi đột ngột, dễ cáu gắt hoặc buồn vui thất thường
            mood_swing = form.cleaned_data['mood_swing']

            # Suy nghĩ về việc tự tử hoặc làm tổn thương bản thân
            suicidal_thoughts = form.cleaned_data['suicidal_thoughts']

            # Biếng ăn, chán ăn hoặc ăn rất ít
            anorexia = form.cleaned_data['anorxia']  # Nên đổi key này thành 'anorexia' để đúng chính tả

            # Mức độ tôn trọng người có thẩm quyền hoặc quy tắc
            authority_respect = form.cleaned_data['authority_respect']

            # Có cố gắng giải thích khi bị hiểu lầm hoặc bị chỉ trích không
            try_explanation = form.cleaned_data['try_explanation']

            # Phản ứng một cách hung hăng khi bị kích động hoặc phản bác
            aggressive_response = form.cleaned_data['aggressive_response']

            # Có xu hướng bỏ qua mọi việc và tiếp tục tiến về phía trước không
            ignore_moveon = form.cleaned_data['ignore_moveon']

            # Có từng trải qua suy sụp tinh thần nghiêm trọng, mất kiểm soát cảm xúc không
            nervous_breakdown = form.cleaned_data['nervous_breakdown']

            # Có dễ dàng thừa nhận lỗi lầm khi mắc sai sót không
            admit_mistakes = form.cleaned_data['admit_mistakes']

            # Có hay suy nghĩ quá mức, lo xa, hoặc bị kẹt trong dòng suy nghĩ tiêu cực không
            overthink = form.cleaned_data['overthink']

            # Mức độ hoạt động tình dục, có bất thường hoặc bị ảnh hưởng bởi trạng thái tinh thần không
            sexual_activity = form.cleaned_data['sexual_activity']

            # Khả năng tập trung vào công việc, học tập, hay thường xuyên bị phân tâm
            concentration = form.cleaned_data['concentration']

            # Mức độ lạc quan trong suy nghĩ, có nhìn nhận tích cực về cuộc sống không
            optimism = form.cleaned_data['optimisim']  # Nên đổi key này thành 'optimism' để đúng chính tả

            new_data = [[sadness, euphoric, exhausted, sleep_disorder,
                        mood_swing, suicidal_thoughts, anorexia, authority_respect,
                        try_explanation, aggressive_response, ignore_moveon,
                        nervous_breakdown, admit_mistakes, overthink, sexual_activity,
                        concentration, optimism
            ]]

            # 4.1.3.7 Nếu dữ liệu hợp lệ: Trích xuất cleaned_data từ form, Mã hóa dữ liệu đầu vào
            new_data = mental_disorder_encoder.transform(new_data)

            # 4.1.3.8 Mô hình học máy dự đoán kết quả bằng dữ liệu đã mã hóa.
            predicted_data = mental_disorder_model.predict(new_data)

            # 4.1.3.9 OrdinalEncoder giải mã kết quả dự đoán.
            prediction_result = mental_disorder_output_encoder.inverse_transform((np.array(predicted_data)).reshape(-1, 1))

            print(prediction_result)

            # Lưu lại lịch sử để lưu báo cáo tại đây

        # 4.1.3.2 Django Web App render prediction form.
        # 4.1.3.3 HTML template hiển thị biểu mẫu thông tin sức khỏe.
        return render(request, 'mental_disorder_prediction.html', {
            'form': form, 'prediction_result': prediction_result[0][0]
        })

    else:
        # Nếu người dùng chỉ truy cập trang, không gửi dữ liệu, thì hiển thị form trống
        # 4.1.3.7a.	Nếu dữ liệu không hợp lệ hoặc thiếu (form không hợp lệ), hệ thống hiển thị lại biểu mẫu kèm theo thông báo lỗi
        form = MentalDisorderForm()

    #     4.1.3.10 Hiển thị kết quả dự đoán trên giao diện người dùng thông qua template kết quả.
    return render(request, 'mental_disorder_prediction.html',
                  {'form': form, 'user_name': request.user.first_name + " " + request.user.last_name})

@login_required
def health_prediction(request):
    return render(request, 'health_test.html', {'user_name': request.user.first_name + " " + request.user.last_name})


def pcos(request):
    return render(request, 'pcos.html',)
