from employee import Employee
from employee_storage import EmployeeWriter
from employee_db import EmployeeDb
import os
import sys

def reset_db(n_employees, file_path):
    if os.path.isfile(file_path): os.remove(file_path)
    with EmployeeWriter(file_path) as db:
        print('Seeding db with data...')
        for i in range(n_employees):
            db.write(Employee.random_employee(i))
        print(f'Populated db with {n_employees} records.')

def main():
    FILE = 'employee-db.bin'
    N_EMPLOYEES = 10000000

    if len(sys.argv) >= 2 and sys.argv[1] == 'reset-db':
        reset_db(N_EMPLOYEES, FILE)

    db = EmployeeDb(FILE)
    db.build_index()

    while True:
        command = input("db> ")
        if command == 'q': break
        elif command == 'list':
            for e in db.list_records(10):
                print(e)
        elif command.startswith('id'):
            id = int(command.split()[1])
            if not db.contains(id):
                print(f'Employee with id {id} does not exist')
                continue
            e = db.get_by_id(id)
            print(e)
        elif command == 'size':
            print(db.size())
        elif command.startswith('del'):
            id = int(command.split()[1])
            if not db.contains(id):
                print(f'Employee with id {id} does not exist')
                continue
            db.delete(id)
            print(f'Record {id} deleted')
        elif command.startswith('update'):
            parts = command.split()[1:]
            e: Employee = None
            for part in parts:
                attr = part.split('=')[0]
                val = part.split('=')[1]
                if attr == 'id': 
                    id = int(val)
                    e = db.get_by_id(id)
                elif attr == 'fname': e.fname = val
                elif attr == 'lname': e.lname = val
                elif attr == 'addr': e.address = val
                elif attr == 'salary': e.salary = int(val)
            db.update(e)
            print(f'Record {e.id} updated')



if __name__ == "__main__":
    main()