from employee import Employee
from employee_storage import EmployeeReader
from typing import Dict, List
import os

class IndexBuilder:
    def __init__(self, file_path):
        self.file_path = file_path

    def index_by_id(self) -> Dict[int, int]:
        if os.path.isfile(self.file_path):
            with EmployeeReader(self.file_path) as file:
                index = {}
                for employee, offset in file:
                    index[employee.id] = offset
                return index
        else:
            return {}

    def index_by_fname(self) -> Dict[str, List[int]]:
        pass