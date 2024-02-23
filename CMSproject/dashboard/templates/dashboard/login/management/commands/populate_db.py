from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import CustomUser, Student, Teacher, Admin, Faculty, Subject, Customer, Order, OrderDetail, MenuItem
import os

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **options):
        # Create Faculty
        computer_faculty = Faculty.objects.create(name='Computer Science')
        civil_faculty = Faculty.objects.create(name='Civil Engineering')

        # Create Students
        student_user1 = CustomUser.objects.create_user(email='student1@example.com', password='12345', usertype='student')
        student1 = Student.objects.create(user=student_user1, name='Student 1', rollNo='077bct039', batch='2077', semester='6', faculty=computer_faculty)
        self.add_profile_picture(student1, 'media/student1.jpg')

        # Create Teachers
        teacher_user1 = CustomUser.objects.create_user(email='teacher1@example.com', password='67890', usertype='teacher')
        teacher1 = Teacher.objects.create(user=teacher_user1, name='Teacher 1')
        self.add_profile_picture(teacher1, 'media/teacher1.jpg')

        # Create Subjects
        subject1 = Subject.objects.create(name='Programming', semester='6')
        subject2 = Subject.objects.create(name='Mathematics', semester='6')

        #Add subjects to faculty
        subject1.faculty.add(computer_faculty, civil_faculty)
        subject2.faculty.add(computer_faculty, civil_faculty)

        # Add Students to Subjects
        subject1.students.add(student1)
        subject2.students.add(student1)

        # Add Teachers to Subjects
        subject1.teachers.add(teacher1)

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
        self.add_image(menu_item1, 'media/cake.webp')  

        # Create Customers for Students
        student_customer1 = Customer.objects.create(student=student1)

        # Create Customers for Teachers
        teacher_customer1 = Customer.objects.create(teacher=teacher1)

        # Create Orders for Students
        order1 = Order.objects.create(customer=teacher_customer1, order_name=menu_item1, quantity=2, status='completed')
        order2 = Order.objects.create(customer=student_customer1, order_name=menu_item2, quantity=1, status='in-progress')

        # Create Order Details for Students
        OrderDetail.objects.create(order=order1, total_amount=menu_item1.price * order1.quantity)
        OrderDetail.objects.create(order=order2, total_amount=menu_item2.price * order2.quantity)

    def add_image(self, instance, file_path):
        with open(file_path, 'rb') as f:
            instance.image.save(os.path.basename(file_path), File(f))
    def add_profile_picture(self, instance, file_path):
        with open(file_path, 'rb') as f:
            instance.profile_picture.save(os.path.basename(file_path), File(f))


