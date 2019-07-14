import os
import json
from datetime import datetime
from typing import NamedTuple, NamedTupleMeta
from app.core import Singleton
from app.storage.exceptions import IntegrityError

DB_PATH = os.path.join(os.path.dirname(__file__), 'db')


class JsonStorageConnection:
    def __init__(self, db_filename):
        self._db_filename = db_filename

    def __enter__(self):
        self.db_file = open(
            os.path.join(DB_PATH, self._db_filename),
            mode='r+',
            encoding='utf-8')
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
                    print('Failed to read db file.')
                record = self._asdict()
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
                json.dump(data, cursor.db_file, indent=4)
                print('inserted record : {}'.format(data))
        except Exception as e:
            print(e)
            raise e


class QuerySet:
    def all(self):
        data = []
        with JsonStorageConnection(
                db_filename=self.Meta.db_filename) as cursor:
            data = json.load(cursor.db_file)
        return data

    def search(self, query):
        pass

    def insert(self):
        pass

    def update(self, query):
        pass

    def remove(self, query):
        pass

    def purge(self):
        pass
