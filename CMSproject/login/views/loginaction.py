from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from core.models import Admin
from django.contrib.sessions.models import Session
from django.views.decorators.cache import never_cache


def login_view(request):
    messages_to_display = request.GET.get('redirect_message', None)
    print(messages_to_display)
    context = {'messages':messages_to_display}
    return render(request, 'login/login.html', context)

def loginaction(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting login with username: {email}, password: {password}")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            print(f"User {user.email} authenticated successfully")
            print(f"Number of users' sessions before login: {len(request.session.keys())}")
            # Login the user
            login(request, user)
            request.session['user_role'] = user.usertype
            request.session['user_id'] = user.id
            usertype = user.usertype

            print(f"Number of users' sessions after login: {len(request.session.keys())}")
            if usertype == 'student':
                return redirect(reverse('s_dashboard'))
            elif usertype == 'teacher':
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

@never_cache
def logout_view(request):
        session_key = request.session.session_key
        if session_key is not None:
        # Delete the session from the database
            Session.objects.filter(session_key=session_key).delete()    
            # Custom logic after logging out
            redirect_message = 'You are successfully logged out'
            redirect_url = reverse('login') + f'?redirect_message={redirect_message}'
            response = redirect(redirect_url)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # Prevent caching
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response