from django.http import JsonResponse
from core.models import Admin, Marks
from django.http import QueryDict
from uuid import UUID
from django.http import Http404
from django.views.decorators.http import require_POST
from examsection.forms.view_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.views import View
from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from django.contrib.auth.decorators import login_required

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
    user = request.user  # Django's authenticated user
    if user.usertype == 'admin':
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

    context = {
        'admin_instance': admin_instance,
        'semester': semester,
        'batch': batch,
        'faculty': faculty,
        'exam_type': exam_type,
        'results': organized_results,
    }

    return render(request, 'examsection/view_result.html', context)