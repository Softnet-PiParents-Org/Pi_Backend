from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

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
    
    
class School(models.Model):
    pass

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    
class Grade(models.Model):
    grade = models.CharField(max_length=4)
    
class Student(models.Model):
    full_name = models.CharField(max_length=255)
    school_ID = models.PositiveIntegerField()
    # profile_pic = models.ImageField(upload_to='/')
    rank = models.PositiveIntegerField()
    average = models.FloatField()
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    
    
    def save(self):
        pass
    

class Subject(models.Model):
    name = models.CharField(max_length=255)
    
    STATUS_INCOMPLETE = 'IC'
    STATUS_PASS = 'P'
    STATUS_FAIL = 'F'

    STATUS_CHOICES = [
        (STATUS_INCOMPLETE, 'Incomplete'),
        (STATUS_PASS, 'Pass'),
        (STATUS_FAIL, 'Fail'), 
    ]

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES)
    
    quiz = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(15.0)])
    test1 = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    mid_exam = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    assignment = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    final_exam = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    semester = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], blank=True, null=True)

    def calculate_final_score(self):
        return (self.quiz * 0.1) + (self.test1 * 0.2) + (self.mid_exam * 0.3) + (self.assignment * 0.1) + (self.final_exam * 0.3)

    def save(self, *args, **kwargs):
        self.score = self.calculate_final_score()
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.student}'


class CourseRecommendation(models.Model):
    course_description=models.TextField()
    release_date=models.DateTimeField(auto_now=True)
    duration=models.PositiveIntegerField()
    
    
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
    #picture = models.ImageField(upload_to='/')
    discription = models.TextField()

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
    #parent as recipent


#chat,reaction in attendance,