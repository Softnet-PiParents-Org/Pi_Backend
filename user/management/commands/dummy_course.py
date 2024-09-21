from django.core.management.base import BaseCommand
from user.models import CourseRecommendation, Subject
import random
import string

class Command(BaseCommand):
    help = 'Fills the CourseRecommendation model with 2-4 recommendations for each subject'


    def generate_random_description(self, min_length=30, max_length=50):
        length = random.randint(min_length, max_length)
        words = string.ascii_lowercase
        return ' '.join(''.join(random.choices(words, k=random.randint(3, 8))) for _ in range(length // 5))
    

    def handle(self, *args, **kwargs):
        subjects = Subject.objects.all()

        posters = [
            "https://imgs.search.brave.com/dYpz7cEL3NKzsLCtYgJpFPJS7V9uCzGgW9w5NAPHj-Y/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTQ0/ODgzNzMwMC9waG90/by91bml2ZXJzaXR5/LXJvYm90aWNzLWxl/Y3R1cmUtYmxhY2st/dGVhY2hlci1leHBs/YWluLWVuZ2luZWVy/aW5nLXRvLXN0dWRl/bnRzLXNoZS11c2Vz/LndlYnA_Yj0xJnM9/MTcwNjY3YSZ3PTAm/az0yMCZjPWwzZzNt/cnYyWFVWdDNUVnct/UzNWNHlnMTgwaFZB/dUs2Q2dkaU43R3c2/dEk9",
            "https://imgs.search.brave.com/HKKeSB0yuduWO5VutU53MQ-70_dK4LPjSm8EISrx_gc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTMy/NzYxMjYyNC9waG90/by90ZWVuYWdlci1n/aXJsLXN0dWR5aW5n/LWF0LWhvbWUuanBn/P3M9NjEyeDYxMiZ3/PTAmaz0yMCZjPVBn/R2RPSEtvREZqX1Ew/eUJPX3hGTjNxVmJ2/RktHQWVaQVVWSDA1/NUQwa009",
            "https://imgs.search.brave.com/U4zSMC4WBaHsWfUPY7CcwKdtcy-45HhsWkWWSHBY9Fs/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTMw/MDgyMjIwNi9waG90/by9hZnJpY2FuLWFt/ZXJpY2FuLWZlbWFs/ZS1zdHVkZW50LXN0/dWR5aW5nLWZyb20t/aG9tZS1hbmQtdGFr/aW5nLW5vdGVzLWZy/b20tcHJvZmVzc29y/LmpwZz9zPTYxMng2/MTImdz0wJms9MjAm/Yz1qWkNhZjF5Zk9I/WDR5NDNZd1JBTmNm/dFFCemh6TXkxbDNW/Q2k5RVlWVHpVPQ",
            "https://imgs.search.brave.com/YWzlUd9vI7BGpfJvZtrrSp6f_cWfIh7_6sDS-PTsHbs/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/dGhvdWdodGNvLmNv/bS90aG1iL3dadV9q/Rk1PUWU3eHVXWXlj/b253cFRxSHZWTT0v/MjUweDAvZmlsdGVy/czpub191cHNjYWxl/KCk6bWF4X2J5dGVz/KDE1MDAwMCk6c3Ry/aXBfaWNjKCkvdGVh/Y2hlci1hbmQtc3R1/ZGVudC1hdC13aGl0/ZS1ib2FyZC1pbi1j/bGFzc3Jvb20tNjc5/NDc2NDk2LTVhYjk5/ZGJkMzEyODM0MDAz/Nzc3OWM1Yy5qcGc",
            "https://imgs.search.brave.com/dcHZyx42jb8ZXnoboxyXdlwazKdNgIhLeffAnAkA6cE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cGl4YWJheS5jb20v/cGhvdG8vMjAxOS8x/Mi8yMS8yMC80NC9t/YXRoLXdvcmstNDcx/MTMwMl82NDAuanBn",
        ]
        links = [
            "https://example.com/course1",
            "https://example.com/course2",
            "https://example.com/course3",
            "https://example.com/course4",
        ]

        for subject in subjects:
            recommendations_count = random.randint(2, 4)
            for _ in range(recommendations_count):
                CourseRecommendation.objects.create(
                    poster=random.choice(posters),
                    course_description=self.generate_random_description(),
                    subject=subject,
                    link=random.choice(links),
                )

        self.stdout.write(self.style.SUCCESS('Successfully added recommendations for all subjects.'))
