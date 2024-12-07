from dataclasses import dataclass
from enum import Enum, auto
from typing import TypedDict, Dict


class Zone(Enum):
    head_and_shoulders = auto()
    back = auto()
    buttocks = auto()
    legs = auto()


class InitializeBedRequest(TypedDict):
    bed_id: int
    sensors: Dict[str, Dict[str, int]]  # zone: {id: int, reading: int}
    actuators: Dict[str, Dict[str, int]]  # zone: {id: int, measurement: int}


class UpdateSensorRequest(TypedDict):
    bed_id: int
    zone: int
    reading: int


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
