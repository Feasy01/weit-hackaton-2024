from fastapi import FastAPI, HTTPException
from typing import Dict
from serwer.models import (
    Bed,
    Zone,
    Sensor,
    Actuator,
    InitializeBedRequest,
    UpdateSensorRequest,
    UpdateActuatorRequest,
    SensorStates,
    ActuatorStates,
    UpdateActuatorQueryAirtable,
    UpdateSensorStateAirtable,
)
from serwer.airtable import AirtableHandler

class BedServer:
    def __init__(self):
        self.app = FastAPI()
        self.beds: Dict[int, Bed] = {}
        self.airtable_handler = AirtableHandler()

        self.register_routes()
        self.initialize_hardcoded_bed()

    def register_routes(self):
        @self.app.post("/initialize_bed")
        async def initialize_bed(request: InitializeBedRequest):
            return await self.initialize_bed(request)

        @self.app.post("/update_sensor")
        async def update_sensor(request: UpdateSensorRequest):
            return await self.update_sensor(request)

        @self.app.post("/update_actuator")
        async def update_actuator(request: UpdateActuatorRequest):
            return await self.update_actuator(request)

        @self.app.get("/bed/{bed_id}")
        async def get_bed(bed_id: int):
            return await self.get_bed(bed_id)

    def initialize_hardcoded_bed(self):
        bed_id = 0
        sensors = {
            Zone.head_and_shoulders: Sensor(id=0, zone=Zone.head_and_shoulders, reading=0),
            Zone.back: Sensor(id=1, zone=Zone.back, reading=0),
            Zone.buttocks: Sensor(id=2, zone=Zone.buttocks, reading=0),
        }

        actuators = {
            Zone.head_and_shoulders: Actuator(id=0, zone=Zone.head_and_shoulders, measurement=0),
            Zone.back: Actuator(id=1, zone=Zone.back, measurement=0),
            Zone.buttocks: Actuator(id=2, zone=Zone.buttocks, measurement=0),
            Zone.legs: Actuator(id=3, zone=Zone.legs, measurement=0),
        }

        self.beds[bed_id] = Bed(id=bed_id, sensors=sensors, actuators=actuators)

    def _determine_actuator_state(self, measurement: int) -> ActuatorStates:
        return ActuatorStates.HIGH if measurement > 50 else ActuatorStates.LOW

    async def update_sensor(self, request: UpdateSensorRequest):
        bed_id = request["bed_id"]
        if bed_id not in self.beds:
            raise HTTPException(status_code=404, detail="Bed not found")
        sensors = {}
        for i, reading in enumerate(request["zone_readings"]):
            sensors[Zone(i)] = SensorStates[reading]

        sensor_states = UpdateSensorStateAirtable(
            bed_id=bed_id,
            head_and_shoulders=sensors[Zone.head_and_shoulders],
            back=sensors[Zone.back],
            buttocks=sensors[Zone.buttocks],
            legs=SensorStates[0],
        )

        self.airtable_handler.upsert_pressure_states(sensor_states)

        return {"message": f"Sensor updated for bed {bed_id}"}

    async def update_actuator(self, request: UpdateActuatorRequest):
        bed_id = request["bed_id"]
        if bed_id not in self.beds:
            raise HTTPException(status_code=404, detail="Bed not found")

        zone = Zone[request["zone"]]
        if zone not in self.beds[bed_id].actuators:
            raise HTTPException(status_code=404, detail="Actuator zone not found")

        self.beds[bed_id].actuators[zone].measurement = request["measurement"]

        actuator_states = UpdateActuatorQueryAirtable(
            bed_id=bed_id,
            head_and_shoulders=self._determine_actuator_state(
                self.beds[bed_id].actuators[Zone.head_and_shoulders].measurement
            ),
            back=self._determine_actuator_state(self.beds[bed_id].actuators[Zone.back].measurement),
            buttocks=self._determine_actuator_state(self.beds[bed_id].actuators[Zone.buttocks].measurement),
            legs=self._determine_actuator_state(self.beds[bed_id].actuators[Zone.legs].measurement),
        )

        self.airtable_handler.update_actuator_measurements(actuator_states)

        return {
            "message": f"Actuator updated for bed {bed_id}, zone {zone.name}",
            "measurement": request["measurement"],
        }

    async def get_bed(self, bed_id: int):
        if bed_id not in self.beds:
            raise HTTPException(status_code=404, detail="Bed not found")

        bed = self.beds[bed_id]
        return {
            "bed_id": bed.id,
            "sensors": {
                zone.name: {"id": sensor.id, "reading": sensor.reading} for zone, sensor in bed.sensors.items()
            },
            "actuators": {
                zone.name: {"id": actuator.id, "measurement": actuator.measurement}
                for zone, actuator in bed.actuators.items()
            },
        }
