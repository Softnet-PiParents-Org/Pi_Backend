import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from user.models import Fee, Parent  

class Command(BaseCommand):
    help = 'Generate random dummy fee data for each parent'

    def handle(self, *args, **kwargs):
        fee_types = ['Tuition', 'Lunch', 'Transport', 'Uniform', 'Book', 'Other']
        fee_status = ['PAID', 'UNPAID']

        parents = Parent.objects.all()

        for parent in parents:
            num_fees = random.randint(6, 15)  
            for _ in range(num_fees):
                fee = Fee(
                    parent=parent,
                    types=random.choice(fee_types),
                    status=random.choice(fee_status),
                    small_desc=f"Fee for {random.choice(fee_types)}",
                    date=datetime.now() - timedelta(days=random.randint(0, 365))  
                )
                fee.save()

            self.stdout.write(self.style.SUCCESS(f"Generated {num_fees} fees for parent {parent.id}"))

        self.stdout.write(self.style.SUCCESS("Dummy fee data generation completed."))
