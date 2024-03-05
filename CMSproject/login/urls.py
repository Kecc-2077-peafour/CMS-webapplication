# login/urls.py
from django.urls import path
from .views.loginaction import login_view , loginaction,CustomLogoutView
from .views.changepassword import newpassword_view, recoverpassword_view

urlpatterns = [
    path ('', login_view , name='login'),
    path('CMSlogin/', loginaction, name='loginaction'),
    path('newpassword/', newpassword_view, name='newpassword'),
    path('recoverpassword/', recoverpassword_view, name='recoverpassword'),
    path('logout/', CustomLogoutView.as_view(), name='custom_logout_view'),
]
