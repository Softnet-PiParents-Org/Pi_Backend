from django.core.management.base import BaseCommand
from user.models import Parent, Teacher, ChatMessage
import random

class Command(BaseCommand):
    help = 'Send chat messages from parents to teachers and vice versa'

    def handle(self, *args, **kwargs):
        parents = Parent.objects.all()
        teachers = Teacher.objects.all()
        messages = [
            "Hello, I have a question about my child's performance.",
            "Could you please share the latest updates regarding assignments?",
            "I'm concerned about the recent class activities.",
            "Thank you for your dedication to our children's education!",
            "When is the next parent-teacher meeting?",
            "I would like to discuss my child's progress.",
            "Please let me know if there are any issues I should be aware of.",
            "I appreciate your efforts in helping my child learn.",
            "Could you provide more resources for my child?",
            "What can I do at home to support my child's learning?"
        ]

        for parent in parents:
            for teacher in teachers:
                if random.choice([True, False]):
                    sender_type = 'parent'
                    ChatMessage.objects.create(
                        sender_type=sender_type,
                        sender_parent=parent,
                        recipient_teacher=teacher,
                        message=random.choice(messages)
                    )
                    self.stdout.write(self.style.SUCCESS(f"Sent message from {parent.full_name} to {teacher.full_name}."))
                else:
                    sender_type = 'teacher'
                    ChatMessage.objects.create(
                        sender_type=sender_type,
                        sender_teacher=teacher,
                        recipient_parent=parent,
                        message=random.choice(messages)
                    )
                    self.stdout.write(self.style.SUCCESS(f"Sent message from {teacher.full_name} to {parent.full_name}."))

        self.stdout.write(self.style.SUCCESS("All messages have been sent between parents and teachers."))
