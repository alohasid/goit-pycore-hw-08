from collections import UserDict
from datetime import datetime
from utils import normalize_phone, get_upcoming_birthdays

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.value = normalize_phone(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.birthday = None

    def remove_phone(self, phone: Phone):
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)
            print(f"Phone {phone} removed from record {self.name}.\n")
        else:
            print(f"Phone {phone} not found in record {self.name}.")

    def add_phone(self, phone: Phone):
        if len(phone.value) == 13:
            self.phones.append(phone)
        else:
            raise ValueError("Phone number must consist of 10 digits.")

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone: Phone):
        for p in self.phones:
            if p.value == phone.value:
                return p
        return None

    def add_birthday(self, birthday: Birthday):
        if self.birthday is None:
            self.birthday = birthday

    def __repr__(self):
        return f"{self.name.value}: {'; '.join(p.value for p in self.phones)}"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_upcoming_birthdays(self):
        return get_upcoming_birthdays(self.data)

    def find(self, name):
        for record in self:
            if name.value.lower() in record.name.value.lower():
                return record  
        return None

    def delete(self, name):
        record = self.find(name)
        if record:
            self.data.pop(name.value)
            return record
        return None
    
    def iterator(self, n):
        for i in range(0, len(self.data), n):
            yield list(self.data.values())[i:i + n]

    def __iter__(self):
        for records in self.iterator(2):
            for record in records:
                yield record

    def __str__(self):
        return '\n'.join(str(record) for record in self)