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

recordsToUpsert = []
for record in inputRecords:
    recordsToUpsert.append( 
        dict(fields=record))

# Read out array sizes
print(f'{len(recordsToUpsert)} records to upsert.')

# Perform record upsert
table.batch_upsert(recordsToUpsert, [AIRTABLE_UNIQUE_FIELD_NAME])

print("\n\nScript execution complete!")