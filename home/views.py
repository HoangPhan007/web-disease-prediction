from urllib import request
from django.shortcuts import get_object_or_404
from .models import Appointment_1
from .models import Doctor_1
import joblib
import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

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


# Danh views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import MedicineReminderForm
from .email_utils import send_medicine_reminder_email

@login_required
def add_reminder(request):
    if request.method == 'POST':
        form = MedicineReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()

            if request.user.email:
                base_url = request.build_absolute_uri('/').rstrip('/')
                send_medicine_reminder_email(reminder, base_url=base_url)

            return redirect('reminder_history')
    else:
        form = MedicineReminderForm()
    return render(request, 'add_reminder.html', {'form': form})



@login_required
def reminder_history(request):
    reminders = MedicineReminder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'reminder_history.html', {'reminders': reminders})


@login_required
def edit_reminder(request, reminder_id):
    reminder = get_object_or_404(MedicineReminder, id=reminder_id, user=request.user)

    if request.method == 'POST':
        form = MedicineReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('reminder_history')  # hoặc tên view hiển thị danh sách
    else:
        form = MedicineReminderForm(instance=reminder)
    
    return render(request, 'edit_reminder.html', {'form': form})

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(MedicineReminder, id=reminder_id, user=request.user)
    if request.method == 'POST':
        name = reminder.medicine_name
        reminder.delete()
        messages.success(request, f'Đã xóa nhắc nhở thuốc "{name}" thành công.')
        return redirect('reminder_history')

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import MedicineReminder

def mark_as_done(request, reminder_id):
    reminder = get_object_or_404(MedicineReminder, id=reminder_id)
    reminder.status = 'done'
    reminder.save()
    messages.success(request, f'Bạn đã đánh dấu thuốc "{reminder.medicine_name}" là đã uống.')
    return redirect('reminder_history')  # hoặc trang phù hợp bạn muốn chuyển đến


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def mark_as_completed(request, reminder_id):
    reminder = get_object_or_404(MedicineReminder, id=reminder_id, user=request.user)
    reminder.status = 'completed'
    reminder.save()
    messages.success(request, "Đã đánh dấu nhắc nhở là hoàn thành.")
    return redirect('reminder_history')  # đổi thành tên url bạn dùng để xem lịch sử


# Phát 
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib import messages

# Xử lý đặt lịch khi người dùng gửi form lịch khám (POST)
# Sequence từng bước 
# Bước 12: Người dùng xác nhận thông tin đặt lịch (gửi form)
# Bước 13: Server nhận thông tin và lưu lịch hẹn vào database
# Bước 15: Hệ thống xác nhận lưu thành công
# Bước 18-19: Server trả trang xác nhận và thông báo thành công cho người dùng

@login_required
def appointment_scheduled(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Appointment_1.objects.create(
                user=request.user,
                full_name=data['full_name'],
                email=data['email'],
                phone=data['phone'],
                doctor=data['doctor'],
                appointment_date=data['appointment_date'],
                appointment_time=data['appointment_time'],
                notes=data['notes']
            )
            messages.success(request, 'Đặt lịch thành công!')
            return redirect('appointment_history')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_scheduled.html', {'form': form})


# Hiển thị danh sách lịch khám của user đã đặt trước đó, sắp xếp mới nhất lên trên
# Bước 19: Người dùng nhận thông báo lịch đã đặt
# Hiển thị dữ liệu lịch sử (dữ liệu đã lưu trước đó)
@login_required
def appointment_history(request):
    appointments = Appointment_1.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'appointment_history.html', {'appointments': appointments})


from django.http import JsonResponse
from django.utils.dateparse import parse_date, parse_time
from datetime import datetime
from .models import Doctor_1, Appointment_1, DoctorSchedule
# Xử lý yêu cầu lấy danh sách bác sĩ còn lịch trống theo ngày giờ được chọn.
# Bước sequence tương ứng:
# Bước 9-11: Người dùng chọn ngày giờ khám
# Server kiểm tra lịch làm việc bác sĩ và lịch đã đặt (lọc bác sĩ trống)
# Trả về danh sách bác sĩ còn trống
def get_available_doctors(request):
    date_str = request.GET.get("date")
    time_str = request.GET.get("time")

    if not date_str or not time_str:
        return JsonResponse({"error": "Missing date or time"}, status=400)

    try:
        appointment_date = parse_date(date_str) 
        appointment_time = parse_time(time_str)
    except Exception:
        return JsonResponse({"error": "Invalid date or time format"}, status=400)

    if not appointment_date or not appointment_time:
        return JsonResponse({"error": "Invalid date or time"}, status=400)

    # Lấy ngày trong tuần (Thứ 2 đến chủ nhật)
    day_of_week = appointment_date.weekday()

    # Tìm bác sĩ có lịch làm việc phù hợp
    working_doctors = Doctor_1.objects.filter(
        schedules__day_of_week=day_of_week,
        schedules__start_time__lte=appointment_time,
        schedules__end_time__gte=appointment_time
    ).distinct()

    # Tìm bác sĩ đã bị đặt lịch tại thời điểm đó
    booked_doctors = Appointment_1.objects.filter(
        appointment_date=appointment_date,
        appointment_time=appointment_time
    ).values_list('doctor_id', flat=True)

    # Loại bỏ bác sĩ đã bị đặt lịch
    available_doctors = working_doctors.exclude(id__in=booked_doctors)

    data = [{"id": doctor.id, "name": str(doctor)} for doctor in available_doctors]
    return JsonResponse(data, safe=False)

