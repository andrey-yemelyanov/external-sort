from typing import List
import unittest
from employee import Employee
from employee_storage import EmployeeReader, EmployeeUpdater, EmployeeWriter
import os

class EmployeeTests(unittest.TestCase):

    def test_serialize(self):
        for id in range(10):
            e = Employee.random_employee(id)
            print(e)
            data = e.serialize()
            self.assertEqual(Employee.EMP_SIZE, len(data))
            deserialized_emp = Employee.deserialize(data)
            self.assertEqual(deserialized_emp.id, e.id)
            self.assertEqual(deserialized_emp.fname, e.fname)
            self.assertEqual(deserialized_emp.lname, e.lname)
            self.assertEqual(deserialized_emp.address, e.address)
            self.assertEqual(deserialized_emp.salary, e.salary)
            self.assertEqual(deserialized_emp.is_deleted, e.is_deleted)

    def test_write_read_employees(self):
        N_EMP = 1000
        FILE = 'employees.bin'

        if os.path.isfile(FILE): os.remove(FILE)

        with EmployeeWriter(FILE) as file:
            for id in range(N_EMP):
                file.write(Employee.random_employee(id))

        with EmployeeReader(FILE) as file:
            size = file.size()
            self.assertEqual(size, N_EMP)
            print(f'{size} records in file {FILE}')
        
        employees: List[Employee] = []
        with EmployeeReader(FILE) as file:
            for e, _ in file: employees.append(e)

        self.assertEqual(len(employees), N_EMP)
        
        for i in range(N_EMP):
            self.assertEqual(employees[i].id, i)

    def test_update_employee(self):
        FILE = 'employees2.bin'

        employees = [
            Employee(100, 'FNAME1', 'LNAME1', 'ADDR1', 1000),
            Employee(101, 'FNAME2', 'LNAME2', 'ADDR2', 1100),
            Employee(102, 'FNAME3', 'LNAME3', 'ADDR3', 1200)
        ]

        if os.path.isfile(FILE): os.remove(FILE)

        with EmployeeWriter(FILE) as file:
            for e in employees: file.write(e)

        with EmployeeReader(FILE) as file:
            e = file.read(Employee.EMP_SIZE)
            self.assertEqual(e.id, employees[1].id)
            self.assertEqual(e.fname, employees[1].fname)
            self.assertEqual(e.lname, employees[1].lname)
            self.assertEqual(e.address, employees[1].address)
            self.assertEqual(e.salary, employees[1].salary)

            e = file.read(Employee.EMP_SIZE * 2)
            self.assertEqual(e.id, employees[2].id)
            self.assertEqual(e.fname, employees[2].fname)
            self.assertEqual(e.lname, employees[2].lname)
            self.assertEqual(e.address, employees[2].address)
            self.assertEqual(e.salary, employees[2].salary)

        e: Employee = None
        with EmployeeReader(FILE) as file:
            e = file.read(Employee.EMP_SIZE)

        e.fname = 'John'
        e.lname = 'Smith'
        e.is_deleted = True
        with EmployeeUpdater(FILE) as fileUpdater:
            fileUpdater.update(e, Employee.EMP_SIZE)

        with EmployeeReader(FILE) as file:
            e = file.read(Employee.EMP_SIZE)
            self.assertEqual(e.id, 101)
            self.assertEqual(e.fname, 'John')
            self.assertEqual(e.lname, 'Smith')
            self.assertEqual(e.address, 'ADDR2')
            self.assertEqual(e.salary, 1100)
            self.assertEqual(e.is_deleted, True)

        with EmployeeReader(FILE) as file:
            self.assertEqual(file.size(), len(employees) - 1)
        