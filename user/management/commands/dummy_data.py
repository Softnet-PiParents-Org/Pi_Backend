import random
from datetime import timedelta, date
from django.core.management.base import BaseCommand
from user.models import Parent, Student, Subject, Result, Absent, PermissionRequest, Teacher

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        parent_names = [
            'Abebe', 'Genet', 'Mulu', 'Hanna', 'Solomon', 
            'Selam', 'Amanuel', 'Rahel', 'Daniel', 'Saba'
        ]
        
        student_names = [
            'Samuel', 'Martha', 'Kebede', 'Tsega', 'Eden',
            'Yared', 'Lily', 'Mekonnen', 'Dagmawi', 'Fikirte',
            'Ayalew', 'Selamawit', 'Hagos', 'Yemane', 'Kassahun',
            'Mekdes', 'Tigist', 'Biruk', 'Amal', 'Simegnew'
        ]

        parents = []
        for name in parent_names:
            parent = Parent.objects.create(
                full_name=name,
                phone=f'2519{random.randint(10000000, 99999999)}',
                password='password123'
            )
            parents.append(parent)

        subjects = ['Mathematics', 'Science', 'History', 'Geography', 'English', 'Physics', 'Chemistry']
        subject_objects = [Subject.objects.create(name=subject) for subject in subjects]

        for parent in parents:
            for grade in [11, 12]:
                for _ in range(20):  # 20 students in each grade
                    student_name = random.choice(student_names)
                    student = Student.objects.create(
                        full_name=f'{student_name} {parent.full_name.split()[0]}',
                        school_ID=random.randint(1000, 9999),
                        rank=random.randint(1, 100),
                        total=100.0,
                        average=100.0,
                        parent=parent,
                        grade=grade
                    )

                    scores = self.generate_scores()
                    for subject in subject_objects:
                        for test_type, score in scores.items():
                            Result.objects.create(
                                student=student,
                                subject=subject,
                                test_type=test_type,
                                score=score
                            )

                    for _ in range(random.randint(0, 5)):
                        absent_date = date.today() - timedelta(days=random.randint(1, 30))
                        Absent.objects.create(student=student, date=absent_date)

                    for _ in range(random.randint(0, 3)):
                        permission_date = date.today() - timedelta(days=random.randint(1, 30))
                        PermissionRequest.objects.create(student=student, date=permission_date)

        for i in range(5):
            Teacher.objects.create(
                full_name=f'Teacher {i + 1} Tesfaye',
                subject=random.choice(subject_objects)
            )

        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))

    def generate_scores(self):
        quiz = random.randint(0, 15)
        assignment = random.randint(0, 10)
        midterm = random.randint(0, 30)
        final = 100 - (quiz + assignment + midterm)

        if final < 0:
            final = 0

        return {
            'quiz': quiz,
            'assignment': assignment,
            'midterm': midterm,
            'final': final
        }
