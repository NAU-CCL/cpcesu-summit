import csv

from django.core.exceptions import ObjectDoesNotExist

from summit.apps.projects.models import Location

with open('park_abbreviations.csv') as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        row_headers = list(row.keys())
        abre = row[row_headers[0]]
        name = row[row_headers[1]]
        print(name + " (" + abre + ")")

        # Check if the park exists.
        # If so, skip
        try:
            cur_loc = Location.objects.get(abbrv=abre)
            if cur_loc is not None:
                pass
            else:
                raise ObjectDoesNotExist()

        # If exception, does not exist so make it
        except ObjectDoesNotExist:
            new_loc = Location(abbrv=abre, name=name)
            new_loc.save()
