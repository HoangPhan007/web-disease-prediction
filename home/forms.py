from django import forms
from .models import Appointment, AppointmentData, obesityDisorder
from .models import MedicineReminder

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date']

from .models import Appointment
# dùng để tạo một lịch hẹn khám (Appointment).
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date']

from .models import mentalDisorder, pcosDisorder
# Dùng để tạo hoặc chỉnh sửa dữ liệu chi tiết liên quan đến cuộc hẹn.
class AppointmentDataForm(forms.ModelForm):
    class Meta:
        model = AppointmentData
        fields = '__all__'
        exclude = ['user', 'doctor', 'status']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control col-md-12'}),
            'phone': forms.TextInput(attrs={'class': 'form-control col-md-12'}),
            'appointmentDate': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

class MentalDisorderForm(forms.ModelForm):
    class Meta:
        model = mentalDisorder
        fields = '__all__'
        exclude = ['user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-md-12'})
            if isinstance(field.widget, forms.Select):
                field.empty_label = "Choose one"

class pcosDisorderForm(forms.ModelForm):
    class Meta:
        model = pcosDisorder
        fields = '__all__'
        exclude = ['user']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-md-12'})
            if isinstance(field.widget, forms.Select):
                field.empty_label = "Choose one"
                
class obesityDisorderForm(forms.ModelForm):
    class Meta:
        model = obesityDisorder
        fields = '__all__'
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-md-12'})
            if isinstance(field.widget, forms.Select):
                field.empty_label = "Choose one"
# Danh forms.py
class MedicineReminderForm(forms.ModelForm):
    class Meta:
        model = MedicineReminder
        fields = [
            'medicine_name',
            'dosage',
            'usage_instructions',
            'start_date',
            'end_date',
            'time_of_day',
            'frequency_per_day',
            'additional_notes',
            'reminder_method',
        ]
        widgets = {
            'medicine_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'usage_instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_of_day': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'frequency_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control'}),
            'reminder_method': forms.Select(attrs={'class': 'form-control'}),
        }
        