from django.urls import path
from .views.exam import examsection_view, handle_course_Info_submisssion, courseInfo_view
from .views.add_result import handle_add_result_submission, addresult_view , submit_result_file
from .views.view_result import handle_view_result_submission, viewresult_view


urlpatterns =[
    path('handle_add_result_submission/', handle_add_result_submission,name='handle_add_result_submission'),
    path('handle_view_result_submission/', handle_view_result_submission,name='handle_view_result_submission'),
    path('handle_course_Info_submission/', handle_course_Info_submisssion,name='handle_course_Info_submission'),
    #path('handle_student_analysis_submission/', handle_filter_submission,name='handle_student_analysis_submission'),
    path('', examsection_view, name='examsection_view'),
    path('addresult/<int:semester>/<int:batch>/<str:faculty>/<str:exam_type>/', addresult_view, name='addresult_view'),
    path('viewresult/', viewresult_view, name='viewresult_view'),
    path('viewcourseInfo/', courseInfo_view, name='courseInfo_view'),
    path('addresultfile/', submit_result_file, name='upload_result_file'),
]