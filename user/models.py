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
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(9), MaxValueValidator(12)]) 

    def __str__(self):
        return self.full_name


class Subject(models.Model):
    name = models.CharField(max_length=255)
    total = models.FloatField(default=0.0, blank=True)

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
    link = models.URLField()

    def __str__(self):
        return self.course_description[:20]
    
    
class Attendance(models.Model):
    STATUS_PRESENT = 'Pr'
    STATUS_ABSENT = 'Ab'
    STATUS_PERMISSION = 'PE'
    
    STATUS_CHOICES = [
        (STATUS_PRESENT,'Present'),
        (STATUS_ABSENT,'Absent'),
        (STATUS_PERMISSION,'Persmission')
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,default= STATUS_PRESENT)
    date = models.DateTimeField(auto_now_add = True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
class PermissionRequest(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField(blank = True,null=True)
    
    class Meta:
        unique_together = ('student', 'date') # one at a time
        
class MissedEvent(models.Model):
    picture = models.ImageField(upload_to='users/images', null= True)
    description = models.TextField()

class Fee(models.Model):
    STATUS_PAID = 'PAID'
    STATUS_UNPAID = 'UNPAID'
    STATUS_CHOICE = [
        {STATUS_PAID,'Paid'},
        {STATUS_UNPAID,'Unpaid'}
    ]
    status = models.CharField(max_length=7,choices=STATUS_CHOICE)
    date = models.DateField()
    
class Notification(models.Model):
    message = models.TextField()
    date = models.DateField()