from django.urls import path
from .views import s_dashboard_view, student_view, teacher_view, viewmyResult_view ,handle_viewmy_result_submission

urlpatterns = [
    path('', s_dashboard_view, name='s_dashboard'),
    path('student/', student_view, name='student_view'),
    path('teacher/', teacher_view, name='teacher_view'),
    path('handle_viewmy_result_submission/', handle_viewmy_result_submission,name='handle_viewmy_result_submission'),
    path('student/viewmyResult', viewmyResult_view, name='viewmyresult'),
]
