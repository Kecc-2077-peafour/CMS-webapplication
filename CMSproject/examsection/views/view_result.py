from django.http import JsonResponse
from core.models import Admin, Marks
from django.http import QueryDict
from uuid import UUID
from django.http import Http404
from django.views.decorators.http import require_POST
from examsection.forms.view_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.views import View
from django.shortcuts import render, redirect
from collections import defaultdict
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse

@csrf_protect
def handle_view_result_submission(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        print(request.POST)

        if form.is_valid():
            filter_metadata = form.get_filter_metadata()
            print("Filter Metadata After Validation:", filter_metadata)
            return JsonResponse({'success': True, 'data': filter_metadata})
        else:
            print("Validation Errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})

@login_required    
def viewresult_view(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin
    
        params = QueryDict(request.GET.urlencode())
        semester = params.get('semester')
        batch = params.get('batch',)
        faculty = params.get('faculty')
        exam_type = params.get('exam_type')
        
        # Build the dynamic query based on the selected filters
        query_params = {}
        if semester is not None:
            query_params['student__semester'] = semester
        if batch is not None:
            query_params['student__batch'] = batch
        if faculty is not None:
            query_params['student__faculty__name'] = faculty
        if exam_type is not None:
            query_params['exam_type'] = exam_type

        results = Marks.objects.filter(**query_params)

        results_by_student = {}
        for result in results:
            student_id = result.student.student_id
            if student_id not in results_by_student:
                results_by_student[student_id] = {'student': result.student, 'subjects': []}
            results_by_student[student_id]['subjects'].append(result)

    # Convert the dictionary values to a list for easier iteration in the template
        organized_results = list(results_by_student.values())
        organized_results = sorted(organized_results, key=lambda x: x['student'].rollNo)
        print("Results after sorting:")
        for result in organized_results:
            print(result)

        context = {
            'admin_instance': admin_instance,
            'semester': semester,
            'batch': batch,
            'faculty': faculty,
            'exam_type': exam_type,
            'results': organized_results,
        }

        return render(request, 'examsection/view_result.html', context)

@login_required
def editresult_view(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin
        try:
            data = json.loads(request.body)
            results_to_update = data.get('data', [])
            # Iterate through the collected data and update the database
            for result_data in results_to_update:
                marks_id = result_data.get('marksId')
                present_data =float(result_data.get('presentData'))

                marks_instance = Marks.objects.get(id=marks_id)
                print(marks_instance)
                # Check if present_data is within valid range
                if 0 <= present_data <=float( marks_instance.subject.full_marks):
                    marks_instance.obtained_marks = present_data
                    marks_instance.marks_updated_by=user
                    marks_instance.save()
                else:
                    response_data = {'success': False, 'message': 'Invalid Data: Please enter valid data'}
                    return JsonResponse(response_data, status=400)
            
            response_data = {'success': True, 'message': 'Edited successfully!'}
            return JsonResponse(response_data)
        except Exception as e:
            print(f'An unexpected error occurred: {e}')
            response_data = {'success': False, 'message': 'An unexpected error occurred'}
            return JsonResponse(response_data, status=500)
    else:
        raise Http404("Admin not found")