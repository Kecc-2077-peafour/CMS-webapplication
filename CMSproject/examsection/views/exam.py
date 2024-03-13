from django.shortcuts import render
from core.models import Admin,Marks,Subject,Student
from uuid import UUID
from django.http import Http404
from examsection.forms.view_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.http import QueryDict
from core.models import Facultysubject
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Value, Case, When, IntegerField
@login_required
def examsection_view(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'admin':
        user = request.user
        messages_to_display = request.GET.get('redirect_message', None)
        print(messages_to_display)
        context = {'admin_instance':user.admin,'messages':messages_to_display}
        return render(request, 'examsection/exam.html', context)
    else:
        raise Http404("Admin not found")
    
@csrf_protect
def handle_course_Info_submisssion(request):
    print(request.method)
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
def courseInfo_view(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin
    
        params = QueryDict(request.GET.urlencode())
        semester = params.get('semester')
        faculty = params.get('faculty')
        print(f'Semester: {semester}, Faculty: {faculty}')

        # Build the dynamic query based on the selected filters
        query_params = {}
        if semester is not None:
            query_params['semester'] = semester
        if faculty is not None:
            query_params['faculty__name'] = faculty

        results = Facultysubject.objects.filter(**query_params)
        for result in results:
            print(f'Faculty: {result.faculty.name}, Semester: {result.semester}, Subjects: {[subject.name for subject in result.subject.all()]}')
        
        if faculty == 'Architecture':
            semester_range = range(1, 11)
        else:
            semester_range = range(1, 9)

        context = {
            'admin_instance': admin_instance,
            'semester': semester,
            'faculty': faculty,
            'results': results,
            'semester_range':semester_range,
        }

        return render(request, 'examsection/courseInfo.html', context)

def handle_analysis_filter_submission(request):
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
    
def student_analysis_view(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin
    
        params = QueryDict(request.GET.urlencode())
        semester = params.get('semester')
        batch = params.get('batch',)
        faculty = params.get('faculty')
        exam_type = params.get('exam_type')
        selected_option = params.get('selectedOption')

        query_params = {}
        if semester is not None:
            query_params['student__semester'] = semester
        if batch is not None:
            query_params['student__batch'] = batch
        if faculty is not None:
            query_params['student__faculty__name'] = faculty
        if exam_type is not None:
            query_params['exam_type'] = exam_type

        # Filter results based on query parameters
        results = Marks.objects.filter(**query_params)
        
        distinct_students = results.values('student').distinct()
        student_percentages = []
        student_list = []
        for student in distinct_students:
            student_id = student['student']
            student_obj = Student.objects.get(student_id=student_id)
            student_list.append(student_obj)
            print(student_obj.name)
            total_subjects = results.filter(student=student_obj).values('subject').distinct().count()
            passed_subjects = results.filter(student=student_obj, obtained_marks__gte=F('subject__pass_marks'))
            pass_percentage = round((passed_subjects.count() / total_subjects),1) * 100 if total_subjects > 0 else 0
            print(pass_percentage)
            fail_percentage = round(100 - pass_percentage,1)
            print(fail_percentage)
            student_percentages.append({
                'student_obj': student_obj,
                'pass_percentage': pass_percentage,
                'fail_percentage': fail_percentage
            })

        total_pass_percentage = round(sum(entry['pass_percentage'] for entry in student_percentages) / len(student_percentages),1)
        total_fail_percentage = round(100 - total_pass_percentage,1)
        print(total_fail_percentage, total_pass_percentage,'theer are total %')


        distinct_subjects = results.values('subject').distinct()
        subject_percentages = []
        subject_list = []
        for subject in distinct_subjects:
            subject_id=subject['subject']
            subject_obj =Subject.objects.get(id=subject_id)
            subject_list.append(subject_obj)
            print(subject_obj.name)
            total_students = results.filter(subject=subject_obj).values('student').distinct().count()
            
            passed_students = results.filter(subject=subject_obj, obtained_marks__gte=F('subject__pass_marks'))
            
            # Calculate pass percentage for this subject
            pass_percentage = round((passed_students.count() / total_students),1) * 100 if total_students > 0 else 0
            print(pass_percentage)
            # Calculate fail percentage for this subject
            fail_percentage = round(100 - pass_percentage,1)
            print(fail_percentage)

            # Store the percentages in the dictionary
            subject_percentages.append({
                'subject_obj': subject_obj,
                'pass_percentage': pass_percentage,
                'fail_percentage': fail_percentage
             })

        context = {
            'admin_instance': admin_instance,
            'student_percentages':student_percentages,
            'subject_percentages':subject_percentages,
            'total_pass_percentage': total_pass_percentage,
            'total_fail_percentage':total_fail_percentage,
            'student_list': student_list,
            'subject_list': subject_list,
        }
        if selected_option == 'subject_analysis':
            return render(request, 'examsection/subject_analysis.html', context)
        elif selected_option == 'student_analysis': 
            return render(request, 'examsection/student_analysis.html', context)