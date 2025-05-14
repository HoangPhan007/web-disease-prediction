from urllib import request

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from pyexpat.errors import messages

from django.shortcuts import render, redirect
from django import forms
from .models import UserProfile


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


# display home page
def index(request):
    return render(request, 'index.html')

# function register call form Register
def register(request):
    if request.method == "POST":
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