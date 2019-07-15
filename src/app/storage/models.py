import json
from datetime import datetime
from typing import NamedTupleMeta, NamedTuple
from app.storage import QuerySet, BaseModel


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
                id: 0,
                registration_number: '',
                color: ''
            }))


class Slot(NamedTuple, BaseModel):
    id: int

    class Meta:
        db_filename = 'slot.json'
        unique_fields = ('id', )

    @classmethod
    def objects(cls):
        return QuerySet(model=cls(**{'id': 0}))

    @classmethod
    def get_empty_slot(cls):
        try:
            parked_slots = {
                parking.slot
                for parking in Parking.objects().all()
            }
        except json.decoder.JSONDecodeError:
            return cls.objects().first()
        all_slots = set(cls.objects().all())
        available_slots = list(all_slots - parked_slots)
        if available_slots:
            return min(available_slots)


class Parking(NamedTuple, BaseModel):
    id: int
    vehicle: Vehicle
    slot: Slot
    parked_at: str
    leave_at: str
    is_empty: bool

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
                    'leave_at': '',
                    'is_empty': True
                }))
