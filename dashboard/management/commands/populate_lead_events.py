from django.core.management.base import BaseCommand
from dashboard.models import Lead, Event

class Command(BaseCommand):
    help = 'Populate the event field in Lead instances based on existing relationships'

    def handle(self, *args, **options):
        # Iterate over each Lead instance
        for lead in Lead.objects.all():
            # Find the corresponding event for the lead's client
            matching_event = Event.objects.filter(client=lead.client).first()

            if matching_event:
                # Associate the event with the lead
                lead.event = matching_event
                lead.save()
                self.stdout.write(self.style.SUCCESS(f"Event associated with Lead: {lead}"))
            else:
                self.stdout.write(self.style.WARNING(f"No matching Event found for Lead: {lead}"))
