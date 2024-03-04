from django.urls import path
from .views import s_dashboard_view, student_view, teacher_view, viewmyResult_view ,handle_viewmy_result_submission,addResult_view,viewResult_view,handle_teacher_add_result_submission,handle_teacher_view_result_submission,submit_result_file_teacher

urlpatterns = [
    path('', s_dashboard_view, name='s_dashboard'),
    path('student/', student_view, name='student_view'),
    path('teacher/', teacher_view, name='teacher_view'),
    path('handle_viewmy_result_submission/', handle_viewmy_result_submission,name='handle_viewmy_result_submission'),
    path('student/viewmyResult/', viewmyResult_view, name='viewmyresult'),
    path('handle_teacher_view_result_submission/', handle_teacher_view_result_submission, name='handle_teacher_view_result'),
    path('handle_teacher_add_result_submission/', handle_teacher_add_result_submission, name='handle_teacher_add_result'),
    path('teacher/addResult/<int:semester>/<int:batch>/<str:faculty>/<str:subject>/', addResult_view, name='teacher_add_result'),
    path('teacher/submit_result_file_teacher', submit_result_file_teacher, name='submit_result_file_teacher'),
    path('teacher/viewResult/', viewResult_view, name='teacher_view_result'),
]
