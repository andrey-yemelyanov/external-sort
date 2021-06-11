from employee_db import EmployeeDb
import unittest
from employee import Employee
from employee_storage import EmployeeWriter
import os

class EmployeeTests(unittest.TestCase):
    
    def test_db(self):
        FILE = 'employees4.bin'

        employees = [
            Employee(100, 'FNAME1', 'LNAME1', 'ADDR1', 1000),
            Employee(101, 'FNAME2', 'LNAME2', 'ADDR2', 1100),
            Employee(102, 'FNAME3', 'LNAME3', 'ADDR3', 1200, is_deleted=True),
            Employee(103, 'FNAME4', 'LNAME4', 'ADDR4', 1300)
        ]

        if os.path.isfile(FILE): os.remove(FILE)

        db = EmployeeDb(FILE)
        for e in employees: db.add(e)
        self.assertEqual(db.size(), len(employees) - 1)
        self.assertRaises(LookupError, lambda: db.get_by_id(102))

        e = db.get_by_id(101)
        self.assertIsNotNone(e)
        self.assertEqual(e.id, employees[1].id)
        self.assertEqual(e.fname, employees[1].fname)
        self.assertEqual(e.lname, employees[1].lname)
        self.assertEqual(e.address, employees[1].address)
        self.assertEqual(e.salary, employees[1].salary)

        updated_employee = db.get_by_id(103)
        updated_employee.fname = 'Jack'
        updated_employee.lname = 'Dawson'
        updated_employee.address = 'Hönögatan 15'
        updated_employee.salary = 0 # pro bono
        db.update(updated_employee)
        e = db.get_by_id(103)
        self.assertIsNotNone(e)
        self.assertEqual(e.fname, updated_employee.fname)
        self.assertEqual(e.lname, updated_employee.lname)
        self.assertEqual(e.address, updated_employee.address)
        self.assertEqual(e.salary, updated_employee.salary)

        db.delete(103)
        self.assertEqual(db.size(), len(employees) - 2)
        self.assertRaises(LookupError, lambda: db.get_by_id(103))

        new_employee = Employee(250, 'Andy', 'Hansson', 'Main St. 123', 1000)
        db.add(new_employee)
        e = db.get_by_id(250)
        self.assertIsNotNone(e)
        self.assertEqual(e.fname, new_employee.fname)
        self.assertEqual(e.lname, new_employee.lname)
        self.assertEqual(e.address, new_employee.address)
        self.assertEqual(e.salary, new_employee.salary)
