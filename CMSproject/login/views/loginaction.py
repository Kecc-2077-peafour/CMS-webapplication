from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from core.models import Admin, Student, Teacher

def login_view(request):
    return render(request, 'login/login.html')

def loginaction(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting login with username: {email}, password: {password}")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Login the user
            print(f"User {user.email} authenticated successfully")
            login(request, user)

            usertype = user.usertype

            if usertype == 'student':
                student = Student.objects.get(user=user)
                return redirect(reverse('s_dashboard'))
            elif usertype == 'teacher':
                teacher = Teacher.objects.get(user=user)
                return redirect(reverse('s_dashboard'))
            elif usertype == 'admin':
                if Admin.objects.filter(user=user).exists():
                    admin_instance = Admin.objects.get(user=user)
                    if admin_instance.role == 'staff':
                        print("Redirecting to canteen")
                        return redirect(reverse('s_canteen'))
                    elif admin_instance.role == 'exam':
                        print("Redirecting to examsection")
                        return redirect(reverse('examsection_view'))
        else:
            print("Authentication failed")

    return render(request, 'login/login.html', {'error_message': 'Invalid login credentials. Please try again.'})
