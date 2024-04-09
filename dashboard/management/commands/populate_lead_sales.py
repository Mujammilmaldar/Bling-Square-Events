from django.core.management.base import BaseCommand
from dashboard.models import Sales, Event , Lead

class Command(BaseCommand):
    help = 'Populate the sales field in Lead instances based on existing relationships'

    def handle(self, *args, **options):
        # Iterate over each Lead instance
        for lead in Lead.objects.all():
            # Find the corresponding sales record for the lead's client
            matching_sales = Sales.objects.filter(client=lead.client).first()

            if matching_sales:
                # Associate the sales record with the lead
                lead.sales = matching_sales
                lead.save()
                self.stdout.write(self.style.SUCCESS(f"Sales record associated with Lead: {lead}"))
            else:
                self.stdout.write(self.style.WARNING(f"No matching sales record found for Lead: {lead}"))
