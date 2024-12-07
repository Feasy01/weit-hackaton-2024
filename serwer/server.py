from fastapi import FastAPI, HTTPException
from typing import Dict
from models import Bed, Zone, Sensor, Actuator, InitializeBedRequest, UpdateSensorRequest, UpdateActuatorRequest

app = FastAPI()

beds: Dict[int, Bed] = {}


def initialize_hardcoded_bed():
    bed_id = 1

    sensors = {
        Zone.head_and_shoulders: Sensor(id=1, zone=Zone.head_and_shoulders, reading=0),
        Zone.back: Sensor(id=2, zone=Zone.back, reading=0),
        Zone.buttocks: Sensor(id=3, zone=Zone.buttocks, reading=0),
    }

    actuators = {
        Zone.head_and_shoulders: Actuator(id=1, zone=Zone.head_and_shoulders, measurement=0),
        Zone.back: Actuator(id=2, zone=Zone.back, measurement=0),
        Zone.buttocks: Actuator(id=3, zone=Zone.buttocks, measurement=0),
        Zone.legs: Actuator(id=4, zone=Zone.legs, measurement=0),
    }

    beds[bed_id] = Bed(id=bed_id, sensors=sensors, actuators=actuators)


initialize_hardcoded_bed()


@app.post("/initialize_bed")
async def initialize_bed(request: InitializeBedRequest):
    bed_id = request.get("bed_id")

    sensors = {}
    actuators = {}

    for zone_str, sensor_data in request["sensors"].items():
        zone = Zone[zone_str.lower()]
        sensors[zone] = Sensor(id=sensor_data["id"], zone=zone, reading=sensor_data["reading"])

    for zone_str, actuator_data in request["actuators"].items():
        zone = Zone[zone_str.lower()]
        actuators[zone] = Actuator(id=actuator_data["id"], zone=zone, measurement=actuator_data["measurement"])

    bed = Bed(id=bed_id, sensors=sensors, actuators=actuators)
    beds[bed_id] = bed

    return {"message": f"Bed {bed_id} initialized successfully"}


@app.post("/update_sensor")
async def update_sensor(request: UpdateSensorRequest):
    bed_id = request["bed_id"]
    if bed_id not in beds:
        raise HTTPException(status_code=404, detail="Bed not found")

    zone = Zone[request.get("zone")]
    if zone not in beds[bed_id].sensors:
        raise HTTPException(status_code=404, detail="Sensor zone not found")

    beds[bed_id].sensors[zone].reading = request["reading"]

    return {"message": f"Sensor updated for bed {bed_id}, zone {zone.name}", "reading": request["reading"]}


@app.post("/update_actuator")
async def update_actuator(request: UpdateActuatorRequest):
    bed_id = request["bed_id"]
    if bed_id not in beds:
        raise HTTPException(status_code=404, detail="Bed not found")

    zone = Zone[request.get("zone")]
    if zone not in beds[bed_id].actuators:
        raise HTTPException(status_code=404, detail="Actuator zone not found")

    beds[bed_id].actuators[zone].measurement = request["measurement"]

    return {"message": f"Actuator updated for bed {bed_id}, zone {zone.name}", "measurement": request["measurement"]}


@app.get("/bed/{bed_id}")
async def get_bed(bed_id: int):
    if bed_id not in beds:
        raise HTTPException(status_code=404, detail="Bed not found")

    bed = beds[bed_id]
    return {
        "bed_id": bed.id,
        "sensors": {zone.name: {"id": sensor.id, "reading": sensor.reading} for zone, sensor in bed.sensors.items()},
        "actuators": {
            zone.name: {"id": actuator.id, "measurement": actuator.measurement}
            for zone, actuator in bed.actuators.items()
        },
    }
