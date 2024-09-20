from django.core.management.base import BaseCommand
from django.utils import timezone
from random import randint, choice
from user.models import Parent, Student, Subject, Result, Absent, PermissionRequest, Teacher, Event

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        parent_names = ['Alice Johnson', 'Bob Smith', 'Catherine Doe', 'David Brown', 'Emma Wilson']
        student_names = ['John', 'Sophia', 'Liam', 'Olivia', 'Mason']
        teacher_names = ['Mr. Anderson', 'Ms. Thomas', 'Mrs. Taylor', 'Mr. Lee', 'Ms. Martin']
        subjects = ['Math', 'English', 'Biology', 'Chemistry', 'History']
        subject_objects = [Subject.objects.create(name=subject) for subject in subjects]

        parents = []
        for name in parent_names:
            parent = Parent.objects.create(
                full_name=name,
                phone=f'2519{randint(10000000, 99999999)}',
                password='password123'
            )
            parents.append(parent)
            self.stdout.write(self.style.SUCCESS(f'Created parent: {name}'))

        for parent in parents:
            for grade in [11, 12]:
                student_name = f'{choice(student_names)} {randint(1, 100)}' 
                student = Student.objects.create(
                    full_name=student_name,
                    school_ID=randint(1000, 9999),
                    rank=randint(1, 5),
                    parent=parent,
                    grade=grade
                )
                student.father_name = parent.full_name  
                student.save()

                self.stdout.write(self.style.SUCCESS(f'Created student: {student_name} with father: {parent.full_name}'))

                for subject in subject_objects:
                    for test_type in ['quiz', 'assignment', 'midterm', 'final']:
                        max_score = {'quiz': 15, 'assignment': 10, 'midterm': 30, 'final': 50}
                        score = randint(10, max_score[test_type])
                        Result.objects.create(
                            test_type=test_type,
                            score=score,
                            student=student,
                            subject=subject
                        )
                        self.stdout.write(self.style.SUCCESS(f'Added result for {student_name} in {subject.name}: {test_type} - {score}'))

                if randint(0, 1):
                    Absent.objects.create(date=timezone.now().date(), student=student)
                    self.stdout.write(self.style.SUCCESS(f'Added absence for {student_name}'))

                if randint(0, 1):
                    PermissionRequest.objects.create(date=timezone.now().date(), student=student)
                    self.stdout.write(self.style.SUCCESS(f'Added permission request for {student_name}'))

        for name, subject in zip(teacher_names, subject_objects):
            Teacher.objects.create(
                full_name=name,
                subject=subject
            )
            self.stdout.write(self.style.SUCCESS(f'Created teacher: {name} for {subject.name}'))

        for i in range(5):
            Event.objects.create(
                picture=None, 
                description=f'Event {i + 1}: Description of the event.'
            )
            self.stdout.write(self.style.SUCCESS(f'Created event: Event {i + 1}'))

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
