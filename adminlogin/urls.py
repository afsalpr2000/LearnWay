from django.urls import path
from .views import Admin_Login

app_name = 'adminlogin'

urlpatterns = [
    path('',Admin_Login,name='adminlogin')
]