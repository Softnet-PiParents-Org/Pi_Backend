from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class ParentManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_("The phone number must be set"))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(phone, password, **extra_fields)


class Parent(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=13, unique=True, null=False, blank=False,
        validators=[
            RegexValidator(
                regex=r'^2519\d{8}$|^09\d{8}$',
                message='Please enter a valid Ethiopian phone number starting with 251 or 09 and followed by 8 digits.'
            )
        ]
    )
    username = None
    email = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = ParentManager()

    def __str__(self):
        return self.phone


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    school_ID = models.PositiveIntegerField(unique=True)
    profile_pic = models.ImageField(upload_to='user/images', blank=True)
    rank = models.PositiveIntegerField()
    total = models.FloatField(default=0.0, blank=True)
    average = models.FloatField(default=0.0, blank=True)
    count = models.PositiveIntegerField(default=0, blank=True)
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(9), MaxValueValidator(12)]) 

    def __str__(self):
        return self.full_name


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Result(models.Model):
    TEST_CHOICES = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('midterm', 'Midterm'),
        ('final', 'Final Exam'),
    ]
    
    test_type = models.CharField(max_length=10, choices=TEST_CHOICES)
    score = models.FloatField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if self.test_type == 'quiz' and not (0.0 <= self.score <= 15.0):
            raise ValidationError('Quiz score must be between 0 and 15.')
        elif self.test_type == 'assignment' and not (0.0 <= self.score <= 10.0):
            raise ValidationError('Assignment score must be between 0 and 10.')
        elif self.test_type == 'midterm' and not (0.0 <= self.score <= 30.0):
            raise ValidationError('Midterm score must be between 0 and 30.')
        elif self.test_type == 'final' and not (0.0 <= self.score <= 50.0):
            raise ValidationError('Final exam score must be between 0 and 50.')

    def __str__(self):
        return f'{self.subject} - {self.student} - {self.test_type}: {self.score}'


class CourseRecommendation(models.Model):
    poster = models.ImageField(upload_to='user/course_recommendation')
    course_description=models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    link = models.URLField()

    def __str__(self):
        return self.course_description[:20]
    
    
class Absent(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.full_name
    

class PermissionRequest(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.full_name


class Teacher(models.Model):
    full_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='user/teacher', blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name} - {self.subject}'


class ChatMessage(models.Model):
    SENDER_TYPE_CHOICES = [
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
    ]

    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE_CHOICES)
    sender_parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)
    sender_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    
    recipient_parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    recipient_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.get_sender()} to {self.get_recipient()} at {self.timestamp}'

    def get_sender(self):
        if self.sender_type == 'parent':
            return self.sender_parent.full_name
        else:
            return self.sender_teacher.full_name

    def get_recipient(self):
        if self.recipient_parent:
            return self.recipient_parent.full_name
        else:
            return self.recipient_teacher.full_name


class Event(models.Model):
    picture = models.ImageField(upload_to='users/images', null= True)
    description = models.TextField()


class Fee(models.Model):
    STATUS_PAID = 'PAID'
    STATUS_UNPAID = 'UNPAID'
    STATUS_CHOICE = [
        {STATUS_PAID,'Paid'},
        {STATUS_UNPAID,'Unpaid'}
    ]
    type = [
        ('Tuition','Tuition'),
        ('Lunch','Lunch'),
        ('Transport','Transport'),
        ('Uniform','Uniform'),
        ('Book','Book'),
        ('Other','Other')
    ]
    status = models.CharField(max_length=7,choices=STATUS_CHOICE)
    types = models.CharField(max_length=255, choices=type, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    

class Notification(models.Model):
    message = models.TextField()
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

