import json
from datetime import datetime
from typing import NamedTupleMeta, NamedTuple
from app.storage import QuerySet, BaseModel


class Vehicle(NamedTuple, BaseModel):
    id: int = 0
    registration_number: str = 'MH-12-BT-0000'
    color: str = 'No Color'
    created_at: str = str(datetime.now().timestamp())
    modified_at: str = str(datetime.now().timestamp())

    objects = QuerySet()

    class Meta:
        db_filename = 'vehicle.json'
        unique_fields = ('registration_number', )

    def __repr__(self):
        return '<Vehicle {0}, id={1}>'.format(self.registration_number,
                                              self.id)


class Slot(NamedTuple, BaseModel):
    slot_number: int

    class NamedTupleMeta:
        filename = 'slot.json'

    def __repr__(self):
        return '<Slot {0}, id={1}>'.format(self.slot_number, self.id)


class Parking(NamedTuple, BaseModel):
    slot: Slot
    vehicle: Vehicle
    parked_at: datetime
    leave_at: datetime

    class NamedTupleMeta:
        filename = 'parking.json'

    def __repr__(self):
        return '<Parking {0}, vehicle={1}, slot={2}>'.format(
            self.id, self.vehicle.registration_number, self.slot.slot_number)
