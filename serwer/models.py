from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict
from typing_extensions import TypedDict


class Zone(Enum):
    head_and_shoulders = 0
    back = 1
    buttocks = 2
    legs = 3


class InitializeBedRequest(TypedDict):
    bed_id: int
    sensors: Dict[str, Dict[str, int]]  # zone: {id: int, reading: int}
    actuators: Dict[str, Dict[str, int]]  # zone: {id: int, measurement: int}


class UpdateSensorRequest(TypedDict):
    bed_id: int
    zone_readings: list[int]


class UpdateActuatorRequest(TypedDict):
    bed_id: int
    zone: int
    measurement: int


@dataclass
class Sensor:
    id: int
    zone: Zone
    reading: int


@dataclass
class Actuator:
    id: int
    zone: Zone
    measurement: int


@dataclass
class Bed:
    id: int
    sensors: Dict[Zone, Sensor]
    actuators: Dict[Zone, Actuator]


SensorStates = ["Ok", "Medium Pressure", "High Pressure", "Very High Pressure"]


class ActuatorStates(Enum):
    LOW = "Low"
    HIGH = "High"


class UpdateActuatorQueryAirtable(TypedDict):
    bed_id: int
    head_and_shoulders: ActuatorStates
    back: ActuatorStates
    buttocks: ActuatorStates
    legs: ActuatorStates


class UpdateSensorStateAirtable(TypedDict):
    bed_id: int
    head_and_shoulders: str
    back: str
    buttocks: str
    legs: str