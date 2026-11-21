
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User

def home(request):
    return render(request, 'accounts/home.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        university_id = request.POST.get('university_id')
        department = request.POST.get('department')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        if User.objects.filter(university_id=university_id).exists():
            messages.error(request, 'University ID already registered.')
            return redirect('register')

        User.objects.create_user(
            email=email,
            password=password,
            university_id=university_id,
            department=department,
            role='STUDENT'
        )

        messages.success(request, 'Registration successful!')
        return redirect('login')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.role == 'STUDENT':
                login(request, user)
                return redirect('dashboard')

            elif user.role == 'STAFF':
                login(request, user)
                return redirect('browse_items')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')

@login_required
def dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('login')

    return render(request, 'accounts/dashboard.html')


def user_logout(request):
    logout(request)
    return redirect('login')