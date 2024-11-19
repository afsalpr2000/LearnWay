from django.urls import path
from .views import Home,Courses,Login,Registration,Forgot_Password,Reset_Password,Otp,Error_Page

app_name = 'homepanel'

urlpatterns = [
    path('',Home, name='home'),
    path('courses/',Courses,name='courses'),
    path('login/',Login,name='login'),
    path('registration/',Registration,name='registration'),
    path('forgot_password/',Forgot_Password,name='forgot_password'),
    path('reset_password/',Reset_Password,name='reset_password'),
    path('otp/',Otp,name='otp'),
    path('404/',Error_Page, name='error_page'),
]