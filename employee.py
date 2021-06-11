import random

class Employee:
    """
    Represents record for storage.
    """

    EMP_SIZE, ID_LEN, FNAME_LEN, LNAME_LEN, ADDR_LEN, SALARY_LEN, IS_DELETED_LEN = 128, 4, 40, 40, 39, 4, 1

    def __init__(self, id: int, fname: str, lname: str, address: str, salary: int, is_deleted: bool = False) -> None:
        """
        Constructor docs.
        """
        self.id = id                    # 4 bytes
        self.fname = fname              # 40 bytes
        self.lname = lname              # 40 bytes
        self.address = address          # 39 bytes
        self.salary = salary            # 4 bytes
        self.is_deleted = is_deleted    # 1 byte

    def random_employee(id: int) -> 'Employee':
        """
        Returns a random Employee object
        """
        fnames = ['John', 'Stacey', 'Brandon', 'Andy', 'Sheila', 'Travis', 'Mike', 'Feruza', 'Ahmed', 'Tony']
        lnames = ['Iöke', 'Blåck', 'Whiåte', 'Bräwn', 'Clänton', 'Åstrovsky', 'Dostoevskyå', 'Tosltoö', 'Hansson', 'Strömberg']
        addresses = ['Brendon St 12', 'Gropegårdsgatan 5tr', 'Styrfarten 1', 'Hagagatan 231', 'Första Långgatan 65A', 'Gamlastaden 134G', 'P.O. Box 283 8562 Fusce Rd.', '7292 Dictum Av.']
        return Employee(id, fnames[random.randint(0, len(fnames) - 1)], lnames[random.randint(0, len(lnames) - 1)], addresses[random.randint(0, len(addresses) - 1)], random.randint(35000, 50000))

    def deserialize(data: bytes) -> 'Employee':
        """
        Decodes 128-byte array into an Employee object
        """
        id = int.from_bytes(data[:Employee.ID_LEN], 'big')
        
        fname_offset = Employee.ID_LEN
        fname = data[fname_offset : fname_offset + Employee.FNAME_LEN].decode().strip()
        
        lname_offset = fname_offset + Employee.FNAME_LEN
        lname = data[lname_offset : lname_offset + Employee.LNAME_LEN].decode().strip()

        addr_offset = lname_offset + Employee.LNAME_LEN
        addr = data[addr_offset : addr_offset + Employee.ADDR_LEN].decode().strip()

        salary_offset = addr_offset + Employee.ADDR_LEN
        salary = int.from_bytes(data[salary_offset : salary_offset + Employee.SALARY_LEN], 'big')

        del_offset = salary_offset + Employee.SALARY_LEN
        is_deleted = True if int.from_bytes(data[del_offset : del_offset + Employee.IS_DELETED_LEN], 'big') == 1 else False
        
        return Employee(id, fname, lname, addr, salary, is_deleted)

    def serialize(self) -> bytes:
        """
        Serializes employee data to a 128-byte array.
        """

        id_bytes = self.id.to_bytes(Employee.ID_LEN, 'big')
        fname_bytes = self.fname.encode()
        lname_bytes = self.lname.encode()
        addr_bytes = self.address.encode()
        salary_bytes = self.salary.to_bytes(Employee.SALARY_LEN, 'big')
        is_deleted_bytes = (1).to_bytes(Employee.IS_DELETED_LEN, 'big') if self.is_deleted else (0).to_bytes(Employee.IS_DELETED_LEN, 'big')

        data = []

        data.extend(id_bytes)

        for i, byte in enumerate(fname_bytes):
            if i == self.FNAME_LEN: break
            data.append(byte)
        data.extend(bytes([32] * (self.FNAME_LEN - len(fname_bytes)))) # pad with whitespace character

        for i, byte in enumerate(lname_bytes):
            if i == self.LNAME_LEN: break
            data.append(byte)
        data.extend(bytes([32] * (self.LNAME_LEN - len(lname_bytes))))

        for i, byte in enumerate(addr_bytes):
            if i == self.ADDR_LEN: break
            data.append(byte)
        data.extend(bytes([32] * (self.ADDR_LEN - len(addr_bytes))))

        data.extend(salary_bytes)
        data.extend(is_deleted_bytes)

        return bytes(data)

    def __str__(self):
        return f'[ID={self.id}, FNAME={self.fname}, LNAME={self.lname}, ADDR={self.address}, SALARY={self.salary}, IS_DELETED={self.is_deleted}]'