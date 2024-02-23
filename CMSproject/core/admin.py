from django.contrib import admin
from .models import Student, Teacher, Admin, CustomUser, Faculty, Subject, Marks,MenuItem,Order,OrderDetail,Facultysubject

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Faculty)
admin.site.register(Facultysubject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Subject)
admin.site.register(Marks)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderDetail)
