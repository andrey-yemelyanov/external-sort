from index import IndexBuilder
from typing import List
import unittest
from employee import Employee
from employee_storage import EmployeeWriter
import os

class EmployeeTests(unittest.TestCase):
    
    def test_index(self):
        FILE = 'employees3.bin'

        employees = [
            Employee(100, 'FNAME1', 'LNAME1', 'ADDR1', 1000),
            Employee(101, 'FNAME2', 'LNAME2', 'ADDR2', 1100),
            Employee(102, 'FNAME3', 'LNAME3', 'ADDR3', 1200, is_deleted=True),
            Employee(103, 'FNAME4', 'LNAME4', 'ADDR4', 1300)
        ]

        if os.path.isfile(FILE): os.remove(FILE)

        with EmployeeWriter(FILE) as file:
            for e in employees: file.write(e)

        index_builder = IndexBuilder(FILE)
        index = index_builder.index_by_id()

        self.assertEqual(len(index), len(employees) - 1)
        self.assertEqual(index, {100: 0, 101: 128, 103: 384})

        print(index)