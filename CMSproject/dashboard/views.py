from django.shortcuts import render
from core.models import Student, Teacher,Marks
from django.http import Http404
from uuid import UUID
from examsection.forms.view_result import FilterForm
from django.http import JsonResponse
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.urls import reverse

@login_required
def s_dashboard_view(request):
    user_role = request.session.get('user_role', None)

    if user_role == 'student':
        context = {'student_instance': request.user.student, 'teacher_instance': None, 'user_type': 'student'}
        return render(request, 'dashboard/s_dashboard.html', context)
    elif user_role == 'teacher':
        context = {'student_instance': None, 'teacher_instance': request.user.teacher, 'user_type': 'teacher'}
        return render(request, 'dashboard/s_dashboard.html', context)
    else:
        raise Http404("Invalid user type")

@login_required
def student_view(request):
    user_role = request.session.get('user_role', None)  # Django's authenticated user

    if user_role == 'student':
        context = {'student_instance': request.user.student}
        return render(request, 'dashboard/student.html', context)
    else:
        raise Http404("Invalid user type")

@login_required
def teacher_view(request):
    user_role = request.session.get('user_role', None)  # Django's authenticated user

    if user_role == 'teacher':
        context = {'teacher_instance': request.user.teacher}
        return render(request, 'dashboard/teacher.html', context)
    else:
        raise Http404("Invalid user type")

@login_required
def handle_viewmy_result_submission(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'student':
        user = request.user
        current_semester = user.student.semester

        if request.method == 'POST': 
            semester = request.POST.get('semester')
            print('yo view ta kahile chalekai xaina?')

            if current_semester >= int(semester):
                filter_metadata = request.POST.dict()
                print("Filter Metadata After Validation:", filter_metadata)
                return JsonResponse({'success': True, 'data': filter_metadata})
            else:
                print('not a valid sem')
                error_message = "Invalid semester. Please enter a semester greater than or equal to the current semester."
                return JsonResponse({'success': False, 'error': error_message}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=500)

def viewmyResult_view(request):
    print('to print my own damn result')
    user_role = request.session.get('user_role', None)
    if user_role == 'student':
        print('authenticated right')
        user = request.user 
        student_instance = user.student
    
        params = QueryDict(request.GET.urlencode())
        semester = params.get('semester')
        exam_type = params.get('exam_type')
        print(semester, exam_type)
        
        current_semester = student_instance.semester
        print('current semester type:', type(current_semester),current_semester)
        print('semester type:', type(semester),semester)

        if semester is not None and int(semester) <= current_semester:
            print('semester is not none')
            semesters = [int(current_semester)]
            query_params = {'student__semester': current_semester, 'exam_type': exam_type}
            results = Marks.objects.filter(**query_params)
            print('query haru we got')
            results_by_student = {}
            for result in results:
                student_id = result.student.student_id
                if student_id not in results_by_student:
                    results_by_student[student_id] = {'student': result.student, 'subjects': []}
                results_by_student[student_id]['subjects'].append(result)
            print('filter vayo?')

            # Convert the dictionary values to a list for easier iteration in the template
            organized_results = list(results_by_student.values())
            for result in organized_results:
                print(result)
            print('context pass vaxa')
            context = {
                'student_instance': student_instance,
                'distinct_semesters': semesters,
                'exam_type': exam_type,
                'organized_results': organized_results,
            }
            return render(request, 'dashboard/student_view_result.html', context)
        elif semester is None:
            print('semester is none')
            # If semester is None, fetch distinct semester values for the student
            distinct_semesters = Marks.objects.filter(student=student_instance).values_list('student__semester', flat=True).distinct()

            # Fetch and organize results for all semesters from 1 to the current semester
            query_params = {'student__semester__in': range(1, current_semester + 1), 'exam_type': exam_type}
            results = Marks.objects.filter(**query_params)
            print('got the quesry')
            results_by_student = {}
            for result in results:
                student_id = result.student.student_id
                if student_id not in results_by_student:
                    results_by_student[student_id] = {'student': result.student, 'subjects': []}
                results_by_student[student_id]['subjects'].append(result)
            print('filter vayo')
            # Convert the dictionary values to a list for easier iteration in the template
            organized_results = list(results_by_student.values())
            for result in organized_results:
                print(result)
            print('context pass vaxa')
            context = {
                'student_instance': student_instance,
                'exam_type': exam_type,
                'organized_results': organized_results,
                'distinct_semesters': distinct_semesters,
            }
            return render(request, 'dashboard/student_view_result.html', context)
        else:
            print('not a valid sem')
            error_message = "Invalid semester. Please enter a semester greater than or equal to the current semester."
            context = {'success': False, 'error_message': error_message}
            return JsonResponse(context, status=400) 
        
def handle_teacher_view_result_submission(request):
    user_role = request.session.get('user_role', None)
    return('sucess')

def handle_teacher_add_result_submission(request):
    user_role = request.session.get('user_role', None)
    return('sucess')
def addResult_view(request):
    return('success')

def viewResult_view(request):
    return('okayy')