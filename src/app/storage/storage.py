import os
import json
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, NamedTupleMeta
from app.core import Singleton
from app.storage.exceptions import IntegrityError

DB_PATH = os.path.join(os.path.dirname(__file__), 'db')


class JsonStorageConnection:
    def __init__(self, db_filename):
        self._db_filename = db_filename

    def __enter__(self):
        file_path = os.path.join(DB_PATH, self._db_filename)
        if not os.path.exists(DB_PATH):
            os.makedirs(DB_PATH)
        filename = Path(file_path)
        filename.touch(exist_ok=True)
        self.db_file = open(file_path, mode='r+', encoding='utf-8')
        return self

    def __exit__(self, *args, **kwargs):
        self.db_file.close()


class MultipleInheritanceNamedTupleMeta(NamedTupleMeta):
    def __new__(mcls, typename, bases, ns):
        if NamedTuple in bases:
            base = super().__new__(mcls, '_base_' + typename, bases, ns)
            bases = (base,
                     *(b for b in bases if not isinstance(b, NamedTuple)))
        return super(NamedTupleMeta, mcls).__new__(mcls, typename, bases, ns)


class BaseModel(metaclass=MultipleInheritanceNamedTupleMeta):
    def save(self, *args, **kwargs):
        try:
            data = list()
            with JsonStorageConnection(
                    db_filename=self.Meta.db_filename) as cursor:
                try:
                    cursor.db_file.seek(0)
                    data = json.load(cursor.db_file)
                except json.decoder.JSONDecodeError:
                    pass
                record = self._asdict()

                # unpack Foreign keys
                for key, value in record.items():
                    if hasattr(value, '_asdict'):
                        record[key] = value._asdict()

                # Check existing record
                for unique_field in self.Meta.unique_fields:
                    if list(
                            filter(
                                lambda x: x[unique_field] == record[unique_field],
                                data)):
                        raise IntegrityError(
                            "{0} '{1}' is already exists.".format(
                                unique_field, record[unique_field]))
                record['id'] = max(map(lambda x: x['id'],
                                       data)) + 1 if data else 1
                data.append(record)
                cursor.db_file.seek(0)
                cursor.db_file.truncate(0)
                json.dump(data, cursor.db_file, indent=4)
        except Exception as e:
            print(e)
            raise e

    def update(self, *args, **kwargs):
        try:
            data = list()
            with JsonStorageConnection(
                    db_filename=self.Meta.db_filename) as cursor:
                try:
                    cursor.db_file.seek(0)
                    data = json.load(cursor.db_file)
                except json.decoder.JSONDecodeError:
                    pass
                record = self._asdict()

                # unpack Foreign keys
                for key, value in record.items():
                    if hasattr(value, '_asdict'):
                        record[key] = value._asdict()

                existing_record = list(
                    filter(lambda item: item['id'] == record['id'], data))
                existing_record_index = data.index(existing_record[0])
                data.pop(existing_record_index)
                data.insert(existing_record_index, record)

                cursor.db_file.seek(0)
                cursor.db_file.truncate(0)
                json.dump(data, cursor.db_file, indent=4)
        except Exception as e:
            print(e)
            raise e

    def get_or_create(self, *args, **kwargs):
        try:
            data = list()
            with JsonStorageConnection(
                    db_filename=self.Meta.db_filename) as cursor:
                try:
                    cursor.db_file.seek(0)
                    data = json.load(cursor.db_file)
                except json.decoder.JSONDecodeError:
                    pass
                record = self._asdict()

                # Check existing record
                existing_record = None
                unique_fields = filter(lambda field: getattr(self, field),
                                       self.Meta.unique_fields)
                for unique_field in unique_fields:
                    try:
                        existing_record = list(
                            filter(
                                lambda x: x[unique_field] == record[unique_field],
                                data))[0]
                        if existing_record:
                            return self._replace(**existing_record)
                    except IndexError:
                        existing_record = None

                # Create new if no existing record
                record['id'] = max(map(lambda x: x['id'],
                                       data)) + 1 if data else 1
                data.append(record)
                cursor.db_file.seek(0)
                cursor.db_file.truncate(0)
                json.dump(data, cursor.db_file, indent=4)
                return self._replace(**record)
        except Exception as e:
            print(e)


class QuerySet:
    def __init__(self, model, *args, **kwargs):
        self._model = model

    def _all_records(self):
        records = []
        data = []
        with JsonStorageConnection(
                db_filename=self._model.Meta.db_filename) as cursor:
            try:
                cursor.db_file.seek(0)
                data = json.load(cursor.db_file)
            except json.decoder.JSONDecodeError:
                pass
        # unpack Foreign keys
        for record in data:
            for key, value in record.items():
                if isinstance(value, dict):
                    model = getattr(self._model, key)
                    record[key] = model(**value)
            records.append(self._model.__class__(**record))
        return records

    def all(self):
        return self._all_records()

    def first(self):
        records = self._all_records()
        if records:
            return records[0]

    def get(self, **kwargs):
        assert kwargs, "Required filter parameters"
        filtered_records = records = self._all_records()
        for key, value in kwargs.items():
            key = key.split('__')
            field, attribute = (key[0], key[1]) if len(key) > 1 else (key[0],
                                                                      None)
            if field not in self._model._fields:
                raise AttributeError(
                    "Invalid field '{0}', available choices are: {1}".format(
                        field, ', '.join(self._model._fields)))

            if field and not attribute:
                filtered_records = set(filter(lambda instance: hasattr(instance, field) and getattr(instance, field) == value, filtered_records))
            elif field and attribute:
                filtered_records = set(filter(lambda instance: hasattr(instance, field) and getattr(getattr(instance, field), attribute) == value, filtered_records))

        if len(filtered_records) > 1:
            raise ValueError(
                "Returning more then 1 value, use 'filter' method instead.")
        elif len(filtered_records) == 1:
            return list(filtered_records)[0]
        else:
            return None

    def filter(self, **kwargs):
        assert kwargs, "Required filter parameters"
        records = self._all_records()
        filtered_records = records
        for key, value in kwargs.items():
            key = key.split('__')
            field, attribute = (key[0], key[1]) if len(key) > 1 else (key[0],
                                                                      None)
            if field not in self._model._fields:
                raise AttributeError(
                    "Invalid field '{0}', available choices are: {1}".format(
                        field, ', '.join(self._model._fields)))

            if field and not attribute:
                filtered_records = set(filter(lambda instance: hasattr(instance, field) and getattr(instance, field) == value, filtered_records))
            elif field and attribute:
                filtered_records = set(filter(lambda instance: hasattr(instance, field) and getattr(getattr(instance, field), attribute) == value, filtered_records))

        return filtered_records

    def insert(self):
        pass

    def update(self, query):
        pass

    def remove(self, query):
        pass

    def purge(self):
        pass
