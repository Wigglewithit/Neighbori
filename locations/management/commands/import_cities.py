import csv
import os
from django.core.management.base import BaseCommand
from locations.models import State, City

class Command(BaseCommand):
    help = "Import U.S. cities into the database from a CSV file."

    def handle(self, *args, **kwargs):
        # Define path to CSV
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, '..', '..', '..', 'data', 'uscities.csv')
        csv_path = os.path.normpath(csv_path)

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found at: {csv_path}"))
            return

        # Begin import
        added_count = 0
        skipped = 0

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                state_name = row.get('state_name')
                state_abbr = row.get('state_id')
                city_name = row.get('city')

                # Optional: skip small towns with < 1000 people
                try:
                    population = int(row.get('population', '0'))
                except ValueError:
                    population = 0

                if population < 1000:
                    skipped += 1
                    continue

                if not state_name or not city_name:
                    skipped += 1
                    continue

                # Get or create State
                state, _ = State.objects.get_or_create(
                    abbreviation=state_abbr.strip(),
                    defaults={'name': state_name.strip()}
                )

                # Add City only if it doesn't exist for this state
                if not City.objects.filter(name=city_name.strip(), state=state).exists():
                    City.objects.create(name=city_name.strip(), state=state)
                    added_count += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import completed: {added_count} cities added, {skipped} skipped."
        ))
