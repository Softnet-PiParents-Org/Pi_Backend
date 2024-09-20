from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from .models import Result, Subject, Student


@receiver(post_save, sender=Result)
@receiver(post_delete, sender=Result)
def update_totals_on_result_change(sender, instance, **kwargs):
    """
    Signal to update the subject's total and student's total and average
    whenever a result is created, updated, or deleted.
    """
    subject = instance.subject
    subject_total = Result.objects.filter(subject=subject).aggregate(models.Sum('score'))['score__sum'] or 0.0
    subject.total = subject_total
    subject.save()

    student = instance.student
    student_results = Result.objects.filter(student=student)
    student_total = student_results.aggregate(models.Sum('score'))['score__sum'] or 0.0
    student.average = student_total / student_results.count() if student_results.count() > 0 else 0.0
    student.total = student_total
    student.save()


@receiver(post_save, sender=Subject)
def update_student_on_subject_change(sender, instance, **kwargs):
    """
    Signal to update the student's total and average when a subject is added
    or its total is modified.
    """
    students_with_subject = Student.objects.filter(result__subject=instance).distinct()
    
    for student in students_with_subject:
        student_results = Result.objects.filter(student=student)
        student_total = student_results.aggregate(models.Sum('score'))['score__sum'] or 0.0
        student.average = student_total / student_results.count() if student_results.count() > 0 else 0.0
        student.total = student_total
        student.save()
