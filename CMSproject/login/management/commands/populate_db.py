from django.core.management.base import BaseCommand
from django.core.files import File
from datetime import date
import random
from core.models import CustomUser, Student, Teacher, Admin, Faculty, Facultysubject,Subject, Order, OrderDetail, MenuItem,Marks
import os

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **options):
        # Create Faculty
        computer_faculty = Faculty.objects.create(name='Computer')
        civil_faculty = Faculty.objects.create(name='Civil')
        subject_applied_mechanics = Subject.objects.create(name='Applied Mechanics', credit_hours=3, full_marks=100, pass_marks=40)
        subject_basic_electronics = Subject.objects.create(name='Basic Electronics', credit_hours=3, full_marks=100, pass_marks=40)
        subject_maths_computer = Subject.objects.create(name='Mathematics', credit_hours=3, full_marks=100, pass_marks=40)

        # Create Facultysubject entry for Computer faculty Semester 6
        facultysubject_computer_semester6 = Facultysubject.objects.create(faculty=computer_faculty, semester=1)
        facultysubject_computer_semester6.subject.add(subject_applied_mechanics, subject_basic_electronics, subject_maths_computer)

        # Create Students
        student_user1 = CustomUser.objects.create_user(email='student1@example.com', password='12345', usertype='student')
        student1 = Student.objects.create(user=student_user1, name='Student 1', rollNo='078bct039', batch='2078', semester=1, faculty=computer_faculty)
        
        student_user2 = CustomUser.objects.create_user(email='student2@example.com', password='12345', usertype='student')
        student2 = Student.objects.create(user=student_user2, name='Student 2', rollNo='078bct001', batch='2078', semester=1, faculty=computer_faculty)

        student_user3 = CustomUser.objects.create_user(email='student3@example.com', password='12345', usertype='student')
        student3 = Student.objects.create(user=student_user3, name='Student 3', rollNo='078bct002', batch='2078', semester=1, faculty=computer_faculty)

        # Create students for Civil Faculty - Semester 1 and 4
        student_user4 = CustomUser.objects.create_user(email='student4@example.com', password='12345', usertype='student')
        student4 = Student.objects.create(user=student_user4, name='Student 4', rollNo='078bct003', batch='2078', semester=1, faculty=civil_faculty)

        student_user5 = CustomUser.objects.create_user(email='student5@example.com', password='12345', usertype='student')
        student5 = Student.objects.create(user=student_user5, name='Student 5', rollNo='078bct004', batch='2078', semester=1, faculty=civil_faculty)
        
        self.add_profile_picture(student1, 'media/student1.jpg')
        self.add_profile_picture(student2, 'media/student1.jpg')
        self.add_profile_picture(student3, 'media/student1.jpg')
        self.add_profile_picture(student4, 'media/student1.jpg')
        self.add_profile_picture(student5, 'media/student1.jpg')

        # Create Teachers
        teacher_user1 = CustomUser.objects.create_user(email='teacher1@example.com', password='67890', usertype='teacher')
        teacher1 = Teacher.objects.create(user=teacher_user1, name='Teacher 1')
        self.add_profile_picture(teacher1, 'media/teacher1.jpg')


        # Create Admins
        admin_user1 = CustomUser.objects.create_user(email='admin1@example.com', password='exam12345', usertype='admin')
        admin1 = Admin.objects.create(user=admin_user1, name='Admin 1', role='exam')
        self.add_profile_picture(admin1, 'media/examadmin1.jpg')

        admin_user2 = CustomUser.objects.create_user(email='admin2@example.com', password='staff12345', usertype='admin')
        admin2 = Admin.objects.create(user=admin_user2, name='Admin 2', role='staff')
        self.add_profile_picture(admin2, 'media/staffadmin1.webp')

        menu_item1 = MenuItem.objects.create(name='Burger', price=200, description='Delicious burger')
        menu_item2 = MenuItem.objects.create(name='pastry', price=60, description='juicy pastry')
        self.add_image(menu_item1, 'media/burger.webp')        
        self.add_image(menu_item2, 'media/cake.webp')  

    def add_image(self, instance, file_path):
        with open(file_path, 'rb') as f:
            instance.image.save(os.path.basename(file_path), File(f))
    def add_profile_picture(self, instance, file_path):
        with open(file_path, 'rb') as f:
            instance.profile_picture.save(os.path.basename(file_path), File(f))


