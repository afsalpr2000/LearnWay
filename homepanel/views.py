from django.shortcuts import render,redirect
from adminpanel.forms import LoginForm,RegistrationForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from adminpanel.models import Profile,Course
from django.db.models import Avg

# Create your views here.

def Home(request):
    return render(request,'homepanel/home.html')

#Courses Demo on Homepanel
def Courses(request):
    all_courses = Course.objects.filter(status='visible').annotate(average_rating=Avg('review__rating')) 
    context = { 
        'all_courses': all_courses,
    }
    return render(request, 'homepanel/courses.html', context)


#Student Login
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    profile = Profile.objects.get(user=user)
                    if profile.is_blocked:
                        messages.error(request, 'Your account is blocked.')
                        return redirect('homepanel:login')
                    elif not user.is_staff and not user.is_superuser:
                        login(request, user)
                        messages.success(request, f'Login Successful as - {user}')
                        return redirect('studentpanel:student_home')
                    else:
                        messages.error(request, 'You are not authorized to login as a student.')
                        return redirect('homepanel:login')
                except Profile.DoesNotExist:
                    messages.error(request, 'Profile does not exist.')
                    return redirect('homepanel:login')
            else:
                messages.error(request, 'Invalid Username or Password!!')
                return redirect('homepanel:login')
    else:
        form = LoginForm()
    return render(request, 'homepanel/login.html', {'form': form})


#Student Registration
def Registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request,'Successfully Registered !!')
            return redirect('studentpanel:student_home')  # Redirect to home or another page after successful registration
        else:
            print("Form is not valid.")
    else:
        form = RegistrationForm()

    return render(request, 'homepanel/registration.html', {'form': form})

def Forgot_Password(request):
    return render(request,'homepanel/forgot_password.html')

def Reset_Password(request):
    return render(request,'homepanel/reset_password.html')

def Otp(request):
    return render(request,'homepanel/otp.html')


def Error_Page(request):
    return render(request, 'homepanel/404.html')
