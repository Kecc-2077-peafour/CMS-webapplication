# CMSproject/urls.py
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from login.views.loginaction import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('examsection/', include('examsection.urls')),
    path('canteen/', include('canteen.urls')),
    path('', login_view, name='main'),
    path('accounts/', include('django.contrib.auth.urls')),
    # Add other urlpatterns if needed
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)