from django.core.management.base import BaseCommand
from user.models import Parent, Student, Grade, Subject, Teacher, Attendance, PermissionRequest, Fee, Notification, MissedEvent, CourseRecommendation
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Populate the database with temp data"

    def handle(self, *args, **kwargs):
        parents = []
        for i in range(10):
            parent = Parent.objects.create_user(
                phone=f'09{random.randint(100000000, 999999999)}', 
                password='password123'
            )
            parents.append(parent)

        grades = []
        for i in range(1, 13):
            grade = Grade.objects.create(grade=f'{i}')
            grades.append(grade)

        students = []
        for i in range(10):
            student = Student.objects.create(
                full_name=f'Student {i + 1}', 
                school_ID=i + 1000,
                rank=random.randint(1, 10),
                average=round(random.uniform(60.0, 90.0), 2),
                parent=parents[i % 10],
                grade=grades[random.randint(0, len(grades) - 1)]
            )
            students.append(student)

        teachers = []
        for i in range(5):
            teacher = Teacher.objects.create(name=f'Teacher {i + 1}')
            teachers.append(teacher)

        subjects = ['Math', 'Science', 'English', 'History', 'Art']
        for student in students:
            for subject in subjects:
                Subject.objects.create(
                    name=subject,
                    quiz=random.uniform(10, 15),
                    test1=random.uniform(60, 100),
                    mid_exam=random.uniform(60, 100),
                    assignment=random.uniform(60, 100),
                    final_exam=random.uniform(60, 100),
                    semester=random.randint(1, 2),
                    teacher=teachers[random.randint(0, len(teachers) - 1)],
                    student=student
                )

        for student in students:
            Attendance.objects.create(
                status=random.choice([Attendance.STATUS_PRESENT, Attendance.STATUS_ABSENT, Attendance.STATUS_PERMISSION]),
                student=student
            )

        for i in range(10):
            PermissionRequest.objects.create(
                parent=parents[i % 10],
                student=students[i],
                date=timezone.now().date(),
                reason=f'Reason {i + 1}'
            )

        for i in range(10):
            Fee.objects.create(
                status=random.choice([Fee.STATUS_PAID, Fee.STATUS_UNPAID]),
                date=timezone.now().date()
            )

        for i in range(10):
            Notification.objects.create(
                message=f'Notification {i + 1}',
                date=timezone.now().date()
            )

        for i in range(10):
            MissedEvent.objects.create(
                description=f'Missed Event {i + 1}'
            )

        for i in range(5):
            CourseRecommendation.objects.create(
                course_description=f'Course {i + 1}',
                duration=random.randint(10, 30)
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with temp data!'))
