import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model

def validate_user_type(value):
        allowed_user_types = ['student', 'teacher', 'admin']
        if value.lower() not in allowed_user_types:
            raise ValidationError(
                _('%(value)s is not a valid user type. Allowed types are student, teacher, and admin.'),
                params={'value': value},
            )
class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, usertype=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, usertype=usertype)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, usertype=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, usertype, **extra_fields)

class CustomUser(AbstractBaseUser):
    #id default hunxa django ma as pk
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    usertype = models.CharField(max_length=20, validators=[validate_user_type])
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        # Check if the user is a staff member (admin)
        return self.is_staff

    def has_module_perms(self, app_label):
        # Check if the user is a staff member (admin)
        return self.is_staff
    
class User(CustomUser):
    class Meta:
        db_table = 'user'

class Subject(models.Model):
    name = models.CharField(max_length=100)
    credit_hours = models.PositiveSmallIntegerField()
    full_marks = models.DecimalField(max_digits=5, decimal_places=2)
    pass_marks = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class Faculty(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Facultysubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)
    semester = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    def __str__(self):
        return f"{self.faculty} - {self.semester}"


class Student(models.Model):
    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rollNo = models.CharField(max_length=10)
    batch =models.CharField(max_length=10)
    semester = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    faculty=models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    notifications = models.ManyToManyField(Notification, related_name='studnet_notifications',blank=True)

    def __str__(self):
        return f"{self.faculty} - {self.name}-{self.semester}"

class Teacher(models.Model):
    teacher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    subject =models.ManyToManyField(Subject)
    notifications = models.ManyToManyField(Notification, related_name='teacher_notifications',blank=True)

    def __str__(self):
        return f"{self.subject}-{self.name}"

class Admin(models.Model):
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    notifications = models.ManyToManyField(Notification, related_name='admin_notifications',blank=True)


    def __str__(self):
        return f"{self.name}-{self.role}"

class Marks(models.Model):
    EXAM_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('back', 'Back'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    exam_date = models.DateField()
    marks_updated_at = models.DateTimeField(auto_now_add=True)
    marks_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def batch(self):
        return self.student.batch

    def __str__(self):
        return f"{self.subject} - {self.student}"

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    special = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    order_name = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('in-progress', 'In-Progress'),
            ('completed', 'Completed'),
            ('pending', 'Pending'),
        ],
        default='pending',
    )

    def __str__(self):
        return f"{self.customer} - {self.status}"
    
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    def save(self, *args, **kwargs):
        self.total_amount = self.order.quantity * self.order.order_name.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order} - {self.total_amount}"

