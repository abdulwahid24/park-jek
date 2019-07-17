import json
from datetime import datetime
from typing import NamedTupleMeta, NamedTuple
from src.app.storage import QuerySet, BaseModel


class Vehicle(NamedTuple, BaseModel):
    id: int
    registration_number: str
    color: str

    class Meta:
        db_filename = 'vehicle.json'
        unique_fields = (
            'id',
            'registration_number',
        )

    @classmethod
    def objects(cls):
        return QuerySet(
            model=cls(**{
                'id': 0,
                'registration_number': '',
                'color': ''
            }))


class Slot(NamedTuple, BaseModel):
    id: int
    is_empty: bool

    class Meta:
        db_filename = 'slot.json'
        unique_fields = ('id', )

    @classmethod
    def objects(cls):
        return QuerySet(model=cls(**{'id': 0, 'is_empty': True}))

    @classmethod
    def get_empty_slot(cls):
        available_slots = set(cls.objects().filter(is_empty=True))
        if not available_slots:
            return None
        return min(available_slots)


class Parking(NamedTuple, BaseModel):
    id: int
    vehicle: Vehicle
    slot: Slot
    parked_at: str
    leave_at: str

    class Meta:
        db_filename = 'parking.json'
        unique_fields = ('id', )

    @classmethod
    def objects(cls):
        return QuerySet(
            model=cls(
                **{
                    'id': 0,
                    'vehicle': Vehicle,
                    'slot': Slot,
                    'parked_at': '',
                    'leave_at': ''
                }))

    @classmethod
    def is_parking_exists(cls, registration_number):
        return cls.objects().get(
            vehicle__registration_number=registration_number, leave_at='')
