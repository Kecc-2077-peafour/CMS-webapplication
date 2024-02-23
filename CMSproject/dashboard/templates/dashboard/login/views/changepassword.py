from django.shortcuts import render

def newpassword_view(request):
    return render(request, 'login/newpassword.html')

def recoverpassword_view(request):
    return render(request, 'login/recovery.html')