from typing import List
from index import IndexBuilder
from employee import Employee
from employee_storage import *
from datetime import datetime
import os

class EmployeeDb:

    def build_index(self):
        print(f'Indexing main file {self.file_path}...')
        start_time = datetime.now()
        self.id_index = IndexBuilder(self.file_path).index_by_id()
        end_time = datetime.now()
        print(f'Indexed {len(self.id_index)} records in {end_time - start_time} seconds')

    def __init__(self, file_path):
        self.file_path = file_path
        self.id_index = {}

    def get_by_id(self, id: int) -> Employee:
        if id not in self.id_index:
            raise LookupError(f'Employee with id {id} does not exist.')
        with EmployeeReader(self.file_path) as reader:
            return reader.read(self.id_index[id])

    def add(self, e: Employee):
        if e.is_deleted: return
        if e.id in self.id_index:
            with EmployeeUpdater(self.file_path) as updater:
                updater.update(e, self.id_index[e.id])
        else:
            with EmployeeWriter(self.file_path) as writer:
                writer.write(e)
            file_size = os.path.getsize(self.file_path)
            self.id_index[e.id] = file_size - Employee.EMP_SIZE

    def update(self, e: Employee):
        if e.id not in self.id_index:
            raise LookupError(f'Employee with id {e.id} does not exist.')
        else:
            with EmployeeUpdater(self.file_path) as updater:
                updater.update(e, self.id_index[e.id])

    def delete(self, id: int):
        if id in self.id_index:
            e: Employee = None
            with EmployeeReader(self.file_path) as reader:
                e = reader.read(self.id_index[id])
            e.is_deleted = True
            with EmployeeUpdater(self.file_path) as updater:
                updater.update(e, self.id_index[id])
            del self.id_index[id]

    def list_records(self, n_records:int) -> List[Employee]:
        records = []
        with EmployeeReader(self.file_path) as reader:
            for e, _ in reader:
                if n_records == 0: break
                records.append(e)
                n_records -= 1
        return records

    def contains(self, id: int) -> bool:
        return id in self.id_index

    def size(self):
        return len(self.id_index)