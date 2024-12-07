# Load dependencies
import os
from pyairtable import Table, Api
import dotenv
from serwer.models import UpdateActuatorQueryAirtable, UpdateSensorStateAirtable


AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE_ID = os.environ["AIRTABLE_TABLE_ID"]
AIRTABLE_UNIQUE_FIELD_NAME = os.environ["AIRTABLE_UNIQUE_FIELD_NAME"]
api = Api(AIRTABLE_API_KEY)


class AirtableHandler:
    def __init__(self) -> None:
        self.table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)

    def update_actuator_measurements(self, input: UpdateActuatorQueryAirtable):
        record = {
            "Bed ID": input["bed_id"],
            "Head And Shoulders": input["head_and_shoulders"].value,
            "Back": input["back"].value,
            "Buttocks": input["buttocks"].value,
            "Legs": input["legs"].value,
        }

        self.batch_upsert([record], [AIRTABLE_UNIQUE_FIELD_NAME])

    def upsert_pressure_states(self, input: UpdateSensorStateAirtable) -> None:
        record = {
            "Bed ID": input["bed_id"],
            "Head And Shoulders Pressure": input["head_and_shoulders"].value if input["head_and_shoulders"] else "Ok",
            "Back Pressure": input["back"].value if input["back"] else "Ok",
            "Buttocks Pressure": input["buttocks"].value if input["head_and_shoulders"] else "Ok",
            "Legs Pressure": input["legs"].value if input["legs"] else "Ok",
        }

        self.batch_upsert([record], [AIRTABLE_UNIQUE_FIELD_NAME])
