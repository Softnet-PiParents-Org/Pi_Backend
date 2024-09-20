from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from user.models import Parent, Fee

class Command(BaseCommand):
    help = 'Fills multiple fee records for all parents'

    def handle(self, *args, **kwargs):
        parents = Parent.objects.all()
        fee_types = ['Tuition', 'Lunch', 'Transport', 'Uniform', 'Book', 'Other']
        
        for parent in parents:
            number_of_fees = random.randint(5, 10)  
            for _ in range(number_of_fees):
                status = random.choice(['PAID', 'UNPAID'])
                fee_type = random.choice(fee_types)
                fee_date = timezone.now() - timezone.timedelta(days=random.randint(0, 60))
                
                Fee.objects.create(
                    status=status,
                    types=fee_type,
                    date=fee_date
                )
                self.stdout.write(self.style.SUCCESS(f"Created Fee for Parent {parent.full_name}: Status - {status}, Type - {fee_type}, Date - {fee_date}"))

        self.stdout.write(self.style.SUCCESS("All fee records have been created for parents."))
