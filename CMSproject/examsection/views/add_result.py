from django.http import JsonResponse
from core.models import Student,Marks,Subject,Facultysubject
from django.views.decorators.http import require_POST
from examsection.forms.add_result import FilterForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404,redirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from decimal import Decimal
import json
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@csrf_protect
def handle_add_result_submission(request):
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
def addresult_view(request, semester, batch, faculty, exam_type):
    user_role = request.session.get('user_role', None)
    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin
        print(semester)
        print(faculty)
        print(batch)
        print(exam_type)
        # total_students = Student.objects.filter(
        #     semester=semester,
        #     faculty__name=faculty,
        #     batch=batch
        # ).count()

        existing_marks = Marks.objects.filter(
            student__semester=semester,
            student__faculty__name=faculty,
            student__batch=batch,
            exam_type=exam_type
        )
        if existing_marks.exists():
            print('duplicate entryy')
            redirect_message = 'Duplicate marks cannot be submitted. Please review and correct your entries.'
            redirect_url = reverse('examsection_view') + f'?redirect_message={redirect_message}'
            return redirect(redirect_url)
        context = {
                'admin_instance': admin_instance,
                'semester': semester,
                'batch': batch,
                'faculty': faculty,
                'exam_type': exam_type,
            }
        return render(request, 'examsection/add_result.html', context)

@login_required
def submit_result_file(request):
    print('i was called')
    user_role = request.session.get('user_role', None)
    if user_role == 'admin':
        user = request.user
    if request.method == 'POST':
        try:
            with transaction.atomic():
                    data = json.loads(request.body.decode('utf-8')).get('data')
                    semester = int(json.loads(request.body.decode('utf-8')).get('semester'))
                    batch = json.loads(request.body.decode('utf-8')).get('batch')
                    faculty = json.loads(request.body.decode('utf-8')).get('faculty')
                    exam_type = json.loads(request.body.decode('utf-8')).get('exam_type')
                    
                    subjects_in_db = Subject.objects.values_list('name', 'full_marks')
                    subjects_in_db_names = [subject[0].lower() for subject in subjects_in_db]
                    subjects_in_file = set(element.lower() for element in data[0][2:]) 
                    print(subjects_in_db_names)
                    print(subjects_in_file)

                    missing_subjects = [subject for subject in subjects_in_file if subject not in subjects_in_db_names]

                    if missing_subjects:
                        raise ValidationError(_('The following subjects do not exist in the database: {}.'.format(', '.join(missing_subjects))))


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
                                subject_full_marks = next(
                                    (full_marks,) for name, full_marks in subjects_in_db if name.lower() == subject_name.lower()
                                )
                                
                                subjects_instance = get_object_or_404(Subject, name = subject_name.lower())
                                if not Facultysubject.objects.filter(
                                    faculty__name=faculty,
                                    semester=semester,
                                    subject__name__iexact=subjects_instance.name.lower(),
                                ).exists():
                                    raise ValidationError(_('{} is not associated with the given faculty and semester',subjects_instance.name))
                                subject_full_marks = subject_full_marks[0]
                                obtained_marks = Decimal(data[roll_numbers_in_file.index(roll_number) + 1][i + 2]) 
                                
                                if not (isinstance(obtained_marks, Decimal) and 0 <= obtained_marks <= subject_full_marks):
                                    raise ValidationError(_('Invalid marks {} for subject {} of student {}. Marks should be an integer between 0 and {}.'.format(obtained_marks, subject_name, roll_number, subject_full_marks)))
                                print('here')
                                Marks.objects.create(
                                    subject=subjects_instance,
                                    student=student,
                                    obtained_marks=obtained_marks,
                                    exam_type=exam_type,
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
       


    

