from django.shortcuts import render
from core.models import Student,Marks,Subject,Facultysubject
from django.http import Http404
from uuid import UUID
from examsection.forms.view_result import FilterForm
from django.http import JsonResponse
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from decimal import Decimal
import json
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from datetime import date

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
    user_role = request.session.get('user_role', None)
    
    if user_role == 'student':
        user = request.user 
        student_instance = user.student

        params = QueryDict(request.GET.urlencode())
        semester = params.get('semester')
        exam_type = params.get('exam_type')

        query_params = {'student': student_instance, 'exam_type': exam_type}

        if semester is not None:
            # If semester is provided, filter results for that semester only
            query_params['student__semester'] = semester
            results = Marks.objects.filter(**query_params)
            distinct_semesters = [int(semester)]
        else:
            # If semester is None, fetch distinct semester values for the student
            distinct_semesters = Marks.objects.filter(student=student_instance).values_list('student__semester', flat=True).distinct()
            # Remove semester filter for fetching all results
            query_params.pop('student__semester', None)
            results = Marks.objects.filter(**query_params)

        print('Filtered Results:')
        for result in results:
            print(f'Student Name: {result.student.name}, Subject: {result.subject.name}, Obtained Marks: {result.obtained_marks}')

        results_by_semester = {}
        for result in results:
            sem = student_instance.semester
            if sem not in results_by_semester:
                results_by_semester[sem] = {'semester': sem, 'subjects': []}

            results_by_semester[sem]['subjects'].append({'subject_name': result.subject.name, 'obtained_marks': result.obtained_marks,'full_marks':result.subject.full_marks,'pass_marks':result.subject.pass_marks})

        # Convert the dictionary values to a list for easier iteration in the template
        organized_results = list(results_by_semester.values())

        context = {
            'student_instance': student_instance,
            'exam_type': exam_type,
            'organized_results': organized_results,
            'distinct_semesters': distinct_semesters,
        }

        return render(request, 'dashboard/student_view_result.html', context)
        
def handle_teacher_view_result_submission(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'teacher':
        teacher_instance = request.user.teacher
        subject_of_teacher = teacher_instance.subject.all()

        if request.method == 'POST':
            for subject in subject_of_teacher:
                print(subject.name) 
            filter_metadata = request.POST.dict()
            subject_entered = request.POST.get('subject_Name')
            print(subject_entered)
            if subject_entered is not None:
                if subject_entered.lower() in [subject.name.lower() for subject in subject_of_teacher]:
                    print(f"{subject_entered} is a valid subject for the teacher.")
                    print("Filter Metadata After Validation:", filter_metadata)
                    return JsonResponse({'success': True, 'data': filter_metadata})
                else:
                    print(f"{subject_entered} is not a valid subject for the teacher.")
                    error_message = "Invalid subject. please enter the subjecyou are associated with only"
                return JsonResponse({'success': False, 'error': error_message}, status=400)
            else:
                print("Filter Metadata After Validation:", filter_metadata)
                return JsonResponse({'success': True, 'data': filter_metadata})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=500)

def handle_teacher_add_result_submission(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'teacher':
        teacher_instance = request.user.teacher
        subject_of_teacher = teacher_instance.subject.all()
        print('Number of subjects associated with the teacher:', subject_of_teacher.count())

        if request.method == 'POST':
            print('yo post ta ho ta ')
            for subject in subject_of_teacher:
                print('database ma vako:',subject) 
            subject_entered = request.POST.get('subject_Name')
            print(subject_entered)
            if subject_entered.lower() in [subject.name.lower() for subject in subject_of_teacher]:
                print(f"{subject_entered} is a valid subject for the teacher.")
                filter_metadata = request.POST.dict()
                batch_entered = request.POST.get('batch_number')
                semester_entered = request.POST.get('semester')
                faculty_entered = request.POST.get('faculty')
                exam_type='regular'
                if not Facultysubject.objects.filter(
                    faculty__name=faculty_entered,
                    semester=semester_entered,
                    subject__name__iexact=subject_entered.lower(),
                ).exists():
                    print(f"{subject_entered} is not associated with the faculty and semester.")
                    error_message = "The entered subject is not associated with the given faculty and semester!"
                    return JsonResponse({'success': False, 'error': error_message}, status=400)
                total_students = Student.objects.filter(
                    semester=semester_entered,
                    faculty__name=faculty_entered,
                    batch=batch_entered
                ).count()
                existing_marks = Marks.objects.filter(
                    student__semester=semester_entered,
                    student__faculty__name=faculty_entered,
                    student__batch=batch_entered,
                    exam_type=exam_type,
                    subject__name=subject_entered,
                )
                print('there marks for: ',semester_entered, faculty_entered, batch_entered,exam_type, subject_entered)
                print('number of marks', existing_marks.count())
                print('no. of students for selected options:',total_students)
                if existing_marks.count() == total_students:
                    print("already value exists")
                    error_message = "The records from the value enetered already exists!"
                    return JsonResponse({'success': False, 'error': error_message}, status=400)
                
                print("Filter Metadata After Validation:", filter_metadata)
                return JsonResponse({'success': True, 'data': filter_metadata})
            else:
                print(f"{subject_entered} is not a valid subject for the teacher.")
                error_message = "Invalid subject. please enter the subject you are associated with only"
                return JsonResponse({'success': False, 'error': error_message}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=500)

def addResult_view(request,semester, batch, faculty, subject):
    user_role = request.session.get('user_role', None)
    if user_role == 'teacher':
        user = request.user
        teacher_instance = user.teacher
        print(semester)
        print(faculty)
        print(batch)
        print(subject)
            
        context = {
            'teacher_instance': teacher_instance,
            'semester': semester,
            'batch': batch,
            'faculty': faculty,
            'subject': subject,
        }
        return render(request, 'dashboard/teacher_add_result.html', context)

def submit_result_file_teacher(request):
    print('i believe i can make it work')
    user_role = request.session.get('user_role', None)
    if user_role == 'teacher':
        user = request.user
        teacher_instance = user.teacher
    if request.method == 'POST':
        try:
            with transaction.atomic():
                    data = json.loads(request.body.decode('utf-8')).get('data')
                    semester = int(json.loads(request.body.decode('utf-8')).get('semester'))
                    batch = json.loads(request.body.decode('utf-8')).get('batch')
                    faculty = json.loads(request.body.decode('utf-8')).get('faculty')
                    subject_entered = json.loads(request.body.decode('utf-8')).get('exam_type')
                    
                    subject_in_file = data[0][2].lower()
                    print(subject_entered,'and the', subject_in_file)
                    # Check if subject_from_json matches subject_in_file
                    if subject_entered.lower() != subject_in_file:
                        raise ValidationError(_('The subject in the file does not match the subject selected to enter.'))

                    students_in_db = Student.objects.values_list('rollNo', 'semester', 'batch', 'faculty')
                    roll_numbers_in_db_rollNo = [str(rollNo[0]) for rollNo in students_in_db] 
                    roll_numbers_in_file = [str(row[0]) for row in data[1:]]  
                    roll_numbers_in_file_sorted = list(roll_numbers_in_file)

                    roll_numbers_in_file_sorted.sort()
                    roll_numbers_in_db_rollNo.sort()
                    print(roll_numbers_in_db_rollNo)
                    print(roll_numbers_in_file)
                    missing_roll_numbers = [roll_number for roll_number in roll_numbers_in_file if roll_number not in roll_numbers_in_db_rollNo]

                    if missing_roll_numbers:
                        raise ValidationError(_('One or more roll numbers do not exist in the database. Missing roll numbers: {}.'.format(', '.join(missing_roll_numbers))))
                    for roll_number in roll_numbers_in_file:
                        student = Student.objects.get(rollNo=roll_number)
                        print(student.semester ,"and", semester)
                        print(student.batch,"and", batch)
                        print(student.faculty.name,"and", faculty)
                        if student.semester != semester or student.batch != batch or str(student.faculty.name) != faculty:
                            raise ValidationError(_('Student {} does not match the provided semester, batch, and faculty.'.format(roll_number)))
                        for i, subject_name in enumerate(data[0][2:]):
                                subject_instance = Subject.objects.get(name__iexact=subject_entered)
    
                                subject_full_marks= subject_instance.full_marks
                                obtained_marks = Decimal(data[roll_numbers_in_file.index(roll_number) + 1][i + 2]) 
                                
                                if not (isinstance(obtained_marks, Decimal) and 0 <= obtained_marks <= subject_full_marks):
                                    raise ValidationError(_('Invalid marks {} for subject {} of student {}. Marks should be an integer between 0 and {}.'.format(obtained_marks, subject_name, roll_number, subject_full_marks)))
                                print('here')
                                print(subject_instance.name,subject_instance.credit_hours)
                                print(teacher_instance.name)
                                Marks.objects.create(
                                    subject=subject_instance,
                                    student=student,
                                    obtained_marks=obtained_marks,
                                    exam_type='regular',
                                    exam_date=date.today(),
                                    marks_updated_by=user,  
                                )
            return JsonResponse({'message': 'Data saved successfully!'}, status=200)    
        except ValidationError as ve:
            import traceback
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': f'Validation error: {str(ve)}', 'error_type': 'validation', 'traceback': traceback_str}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': f'Error saving data: {str(e)}', 'error_type': 'processing'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def viewResult_view(request):
    user_role = request.session.get('user_role', None)
    if user_role == 'teacher':
        teacher_instance = request.user.teacher
        params = QueryDict(request.GET.urlencode())
        semester = params.get('semester')
        batch = params.get('batch_number')
        faculty = params.get('faculty')
        subject = params.get('subject_Name')
        query_params = {}
        if semester is not None:
            query_params['student__semester'] = semester
        if batch is not None:
            query_params['student__batch'] = batch
        if faculty is not None:
            query_params['student__faculty__name'] = faculty
        if subject is not None:
            query_params['subject__name'] = subject
        if subject is None:
            query_params['subject__name__in'] = teacher_instance.subject.values_list('name', flat=True)

        results = Marks.objects.filter(**query_params)

        results_by_student = {}
        for result in results:
            student_id = result.student.student_id
            if student_id not in results_by_student:
                results_by_student[student_id] = {'student': result.student, 'subjects': []}
            results_by_student[student_id]['subjects'].append(result)
            print(f"Result: {result}")
        organized_results = list(results_by_student.values())
        organized_results = sorted(organized_results, key=lambda x: x['student'].rollNo)
        print("Results after sorting:")
        for result in organized_results:
            print(result)
        context = {
            'teacher_instance': teacher_instance,
            'semester': semester,
            'batch': batch,
            'faculty': faculty,
            'subject': subject,
            'results': organized_results,
        }

        return render(request, 'dashboard/teacher_view_result.html', context)