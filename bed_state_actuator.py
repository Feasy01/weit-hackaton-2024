# Load dependencies
import os
from pyairtable import Table, Api  # to interact with Airtable REST API
from dotenv import load_dotenv  # to load .env files with environment variables

# Load .env file
load_dotenv()

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
AIRTABLE_TABLE_ID = os.environ['AIRTABLE_TABLE_ID']
AIRTABLE_UNIQUE_FIELD_NAME = os.environ['AIRTABLE_UNIQUE_FIELD_NAME']

api = Api(AIRTABLE_API_KEY)
table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)

inputRecords = [
    {
        'Bed ID': '1',
        'Head And Shoulders Pressure': 'Ok',
        'Back Pressure': 'Medium Pressure',
        'Buttocks Pressure': 'High Pressure',
        'Legs Pressure': 'Very High Pressure',
        'Head And Shoulders State': 'Low',
        'Back State': 'High',
        'Buttocks State': 'Low',
        'Legs State': 'Low'
    }
]

'''
Opis działania na potrzeby Hackatonu:
W cykly co 30 sekund powinno wydarzyć się:
- reset stanów serwo do stanu początkowego (stan początkowy mozna najławiej opisać prostym materacem bez zadnych wybrzuszeń)
- zebranie pomiarow z belek 
    - porównanie pomiarów między sobą:
        - obszar z najnizszym naciskiem: 'Ok'
        - obszar w kolejnym naciskiem: 'Medium pressure'
        - obszar z prawie najwyzszym naciskiem: 'High Pressure'
        - obszar z najwyzszym naciskiem: 'Very High Pressure'
- strefy wokół strefy z najwyzszym naciskiem zostają podniesione
- do apki trafiają informacje:
    - o stanach nacisku na danym obszarze zgodnie z powyzszym opisem
    - o stanie podniesienia stref:
        - wszystkie niepodniesine: "Low"
        - strefa podniesiona: "High"

'''

recordsToUpsert = []
for record in inputRecords:
    recordsToUpsert.append( 
        dict(fields=record))

# Read out array sizes
print(f'{len(recordsToUpsert)} records to upsert.')

# Perform record upsert
table.batch_upsert(recordsToUpsert, [AIRTABLE_UNIQUE_FIELD_NAME])

print("\n\nScript execution complete!")