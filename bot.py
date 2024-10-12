import sys
import os
import pickle
from addressbook import AddressBook, Birthday, Record, Name, Phone

FILENAME = "addressbook.pkl"

def save_data(book, filename=FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=FILENAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Error: Give me correct arguments."
        except KeyError:
            return "Error: Contact not found."
        except IndexError:
            return "Error: Enter the argument for the command"
        except Exception as e:
            return f"Unexpected error: {e}"

    return inner


def parse_input(user_input):
    parts = user_input.strip().lower().split()
    command = parts[0]
    arguments = parts[1:]
    return command, arguments

@input_error
def add_contact(arguments, book):
    if len(arguments) < 2:
        raise ValueError("Name and phone are required.")
    
    name, phone = arguments
    record = book.find(Name(name))
    
    if len(phone) != 10:
        raise ValueError("Phone number must consist of 10 digits.")
    elif record is None:
        record = Record(Name(name))
        record.add_phone(Phone(phone))
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    
    return message

@input_error
def change_contact(arguments, book):
    if len(arguments) < 2:
        raise ValueError("Name and new phone number are required.")
    
    name, phone = arguments
    record = book.find(Name(name))
    
    if record:
        record.edit_phone(Phone(record.phones[0].value), Phone(phone))
        return "Contact updated."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def remove_contact(arguments, book):
    if not arguments:
        raise IndexError("Name is required for removing a contact.")
    
    name = arguments[0]
    record = book.find(Name(name))
    
    if record:
        book.delete(Name(name))
        return "Contact deleted."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def show_phone(arguments, book):
    if not arguments:
        raise IndexError("Name is required to show phone.")
    
    name = arguments[0]
    record = book.find(Name(name))
    
    if record:
        return f"{record.name.value}: {', '.join(p.value for p in record.phones)}"
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def show_all(book):
    if book:
        return "\n".join(f"{record}" for record in book)
    else:
        return "No contacts found."


@input_error
def add_birthday(arguments, book):
    if len(arguments) < 2:
        raise ValueError("Name and birthday are required.")
    
    name, birthday = arguments
    record = book.find(Name(name))
    
    if record:
        record.add_birthday(Birthday(birthday))
        return "Birthday added."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def show_birthday(arguments, book):
    if not arguments:
        raise IndexError("Name is required to show birthday.")
    
    name = arguments[0]
    record = book.find(Name(name))
    
    if record:
        return f"{record.name.value}'s birthday: {record.birthday.value}" if record.birthday else "Birthday not set."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def birthdays(arguments, book):
    if arguments:
        name = arguments[0]
        record = book.find(Name(name))
        
        if record:
            return record.get_all_upcoming_birthdays()
        else:
            raise KeyError(f"Contact {name} not found.")
    else:
        return book.get_all_upcoming_birthdays()
def main():
    contacts = load_data(FILENAME)
    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter command: ")
            command, arguments = parse_input(user_input)

            if command == "hello":
                print("How can I help you?")
            
            elif command == "add":
                print(add_contact(arguments, contacts))
            
            elif command == "change":
                print(change_contact(arguments, contacts))

            elif command == "remove":
                print(remove_contact(arguments, contacts))
            
            elif command == "phone":
                print(show_phone(arguments, contacts))
            
            elif command == "all":
                print(show_all(contacts))

            elif command == 'add_birthday':
                print(add_birthday(arguments, contacts))
            
            elif command == 'show_birthday':
                print(show_birthday(arguments, contacts))

            elif command == 'birthdays':
                print(birthdays(arguments, contacts))
            
            elif command in ["close", "exit"]:
                print("Good bye!")
                break
            
            else:
                print("Invalid command.")

    except KeyboardInterrupt:
        print("\nGood bye!")
    finally:
        save_data(contacts, FILENAME)


if __name__ == "__main__":
    main()
    
    