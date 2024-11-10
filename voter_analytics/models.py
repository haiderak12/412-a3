from django.db import models
import os

# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data from one registered voter in Newton, MA.
    '''
    # Identification
    voter_id_number = models.CharField(max_length=20)
    first_name = models.TextField()
    last_name = models.TextField()
    # Address
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(null=True, blank=True)
    zip_code = models.TextField()
    # Dates
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    # Party and Precinct
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    # Voting History
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()
    
    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.street_name}, {self.zip_code})'
    
def load_data():
    '''Load data records from a CSV file into model instances.'''

    # Delete all existing records to avoid duplicates
    Voter.objects.all().delete()
    
    # Open the CSV file for reading
    import os
    app_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(app_dir, 'newton_voters.csv')
    f = open(filename, encoding='utf-8')
    headers = f.readline()  # Read and discard the header line
    print(f'Headers: {headers}')
    
    # Loop to read all the lines in the file
    for line in f:
        try:
            fields = line.strip().split(',')  # Create a list of fields
            # Ensure we have the correct number of fields
            if len(fields) < 17:
                print(f'Skipping line due to incorrect number of fields: {line}')
                continue

            # Parse and clean fields
            def parse_bool(value):
                return value.strip().lower() in ('1', 'true', 'yes')

            def parse_date(value):
                from datetime import datetime
                try:
                    return datetime.strptime(value.strip(), '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return None

            # Create a new instance of Voter with data from CSV
            voter = Voter(
                voter_id_number=fields[0].strip(),
                last_name=fields[1].strip(),
                first_name=fields[2].strip(),
                street_number=fields[3].strip(),
                street_name=fields[4].strip(),
                apartment_number=fields[5].strip() if fields[5].strip() else None,
                zip_code=fields[6].strip(),
                date_of_birth=parse_date(fields[7]),
                date_of_registration=parse_date(fields[8]),
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10].strip(),
                v20state=parse_bool(fields[11]),
                v21town=parse_bool(fields[12]),
                v21primary=parse_bool(fields[13]),
                v22general=parse_bool(fields[14]),
                v23town=parse_bool(fields[15]),
                voter_score=int(fields[16].strip()),
            )
            voter.save()  # Save this instance to the database
            print(f'Created voter: {voter}')

        except Exception as e:
            print(f"Exception on line: {line}")
            print(f"Error: {e}")
