from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login
from adminpanel.forms import LoginForm,RegistrationForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from adminpanel.models import Profile

# Create your views here.

def Admin_Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                profile = Profile.objects.get(user=user)
                if user is not None and user.is_staff and not user.is_superuser: 
                    auth_login(request, user)
                    messages.success(request,f'Login Successful as - {user}')
                    return redirect('adminpanel:admin_home')
                else:
                    messages.error(request, 'You are not authorized to login as Admin.')
                    return redirect('adminlogin:adminlogin')
            else:
                messages.error(request, 'Invalid Username or Password!!')
                return redirect('adminlogin:adminlogin')
    else:
        form = LoginForm()
    return render(request,'adminlogin/adminlogin.html',{'form':form})