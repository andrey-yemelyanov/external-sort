from employee import Employee
import os

class EmployeeWriter:

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'ab')
        return self
  
    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()

    def write(self, e: Employee):
        self.file.write(e.serialize())

class EmployeeUpdater:

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'r+b')
        return self
  
    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()

    def update(self, e: Employee, offset: int):
        self.file.seek(offset)
        self.file.write(e.serialize())

class EmployeeReader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.offset = - Employee.EMP_SIZE

    def __enter__(self):
        self.file = open(self.file_path, 'br')
        return self
  
    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()

    def __iter__(self):
        return self

    def __next__(self):
        self.offset += Employee.EMP_SIZE
        data = self.file.read(Employee.EMP_SIZE)
        if len(data) == 0 : raise StopIteration
        e = Employee.deserialize(data)
        if e.is_deleted: return self.__next__()
        return (e, self.offset)

    def read(self, offset):
        self.file.seek(offset)
        data = self.file.read(Employee.EMP_SIZE)
        return Employee.deserialize(data)

    def size(self):
        count = 0
        for e, _ in self: 
            if not e.is_deleted: count += 1
        return count