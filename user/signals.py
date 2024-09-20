from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import *
import heapq
from collections import defaultdict

@receiver(post_save, sender=Result)
@receiver(post_delete, sender=Result)
def update_student_on_result_change(sender, instance, **kwargs):
    """
    Signal to update the student's total and average whenever a result is created, updated, or deleted.
    Takes into account the grade of the student for calculations.
    """
    student = instance.student
    score = instance.score

    student.total += score
    student.save()

    total = Subject.objects.count()
    student.average = ((student.total / (total * 100)) * 100) if total > 0 else 0.0

    calculate_student_rank()

    # Save the student instance
    student.save()


def calculate_student_rank():
    """
    Custom logic for calculating a student's rank based on their total score and grade.
    This function considers students in the same grade for ranking.
    """
    table = defaultdict(list)
    all_students = Student.objects.all()
    for student in all_students:
        heapq.heappush(table[student.grade], [student.total, student])
    for grade in table:
        rank = 1
        while table[grade]:
            total, student = heapq.heappop(table[grade])
            student.rank = rank
            student.save()
            rank += 1

@receiver(post_save, sender=Result)
def create_result_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f"New result submitted for {instance.student.full_name} in {instance.subject.name}",
            parent=instance.student.parent
        )


@receiver(post_save, sender=Absent)
def create_absent_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f"{instance.student.full_name} was marked absent on {instance.date}.",
            parent=instance.student.parent
        )

@receiver(post_save, sender=PermissionRequest)
def create_permission_request_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f"{instance.student.full_name} has requested permission for {instance.date}.",
            parent=instance.student.parent
        )



@receiver(post_save, sender=ChatMessage)
def create_chat_message_notification(sender, instance, created, **kwargs):
    if created:
        if instance.sender_type == 'parent':
            Notification.objects.create(
                message=f"New message from parent {instance.sender_parent.full_name} to teacher {instance.recipient_teacher.full_name}.",
                parent=instance.recipient_teacher.parent
            )
        else:
            Notification.objects.create(
                message=f"New message from teacher {instance.sender_teacher.full_name} to parent {instance.recipient_parent.full_name}.",
                parent=instance.recipient_parent
            )


@receiver(post_save, sender=Event)
def create_event_notification(sender, instance, created, **kwargs):
    if created:
        for parent in Parent.objects.all():
            Notification.objects.create(
                message=f"New event created: {instance.description[:20]}...",
                parent=parent
            )

@receiver(post_save, sender=Fee)
def create_fee_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f"Fee status updated to {instance.get_status_display()} on {instance.date}.",
            parent=instance.student.parent 
        )