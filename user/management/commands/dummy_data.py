import random
from datetime import timedelta, date
from django.core.management.base import BaseCommand
from user.models import Parent, Student, Subject, Result, Absent, PermissionRequest, Teacher

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        parents = []
        for i in range(10):
            parent = Parent.objects.create(
                full_name=f'Parent {i + 1}',
                phone=f'2519{random.randint(10000000, 99999999)}',
                password='password123'
            )
            parents.append(parent)

        subjects = ['Mathematics', 'Science', 'History', 'Geography', 'English', 'Physics', 'Chemistry']
        subject_objects = [Subject.objects.create(name=subject) for subject in subjects]

        for parent in parents:
            for grade in range(9, 13):
                for _ in range(random.randint(1, 4)):
                    student = Student.objects.create(
                        full_name=f'Student {parent.full_name}',
                        school_ID=random.randint(1000, 9999),
                        rank=random.randint(1, 100),
                        total=100.0,
                        average=100.0,
                        parent=parent,
                        grade=grade
                    )
                    for subject in subject_objects:
                        for test_type in ['quiz', 'assignment', 'midterm', 'final']:
                            Result.objects.create(
                                student=student,
                                subject=subject,
                                test_type=test_type,
                                score=100.0
                            )

                    for _ in range(random.randint(0, 5)):
                        absent_date = date.today() - timedelta(days=random.randint(1, 30))
                        Absent.objects.create(student=student, date=absent_date)

                    for _ in range(random.randint(0, 3)):
                        permission_date = date.today() - timedelta(days=random.randint(1, 30))
                        PermissionRequest.objects.create(student=student, date=permission_date)

        for i in range(5):
            Teacher.objects.create(
                full_name=f'Teacher {i + 1}',
                subject=random.choice(subject_objects)
            )

        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))
