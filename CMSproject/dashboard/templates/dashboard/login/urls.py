# login/urls.py
from django.urls import path
from .views.loginaction import login_view , loginaction
from .views.changepassword import newpassword_view, recoverpassword_view

urlpatterns = [
    path ('', login_view , name='login'),
    path('loginaction/', loginaction, name='loginaction'),
    path('newpassword/', newpassword_view, name='newpassword'),
    path('recoverpassword/', recoverpassword_view, name='recoverpassword'),
]
