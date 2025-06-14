import json
import os
import sys 


def load_notes(filename="notes.json"):

    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:

            if os.path.getsize(filename) > 0:
                return json.load(f)
            else:
                return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_notes(notes, filename="notes.json"):
    with open(filename, 'w') as f:
        json.dump(notes, f, indent=4)


def list_notes(filename="notes.json"):
    
    notes = load_notes(filename)
    if not notes:
        print("Your note is empty!")
        return

    print("--- Your Notes ---")
    for note in notes:
        print(f"[{note['id']}] {note['text']}")
    print("------------------")


def add_note(text, filename="notes.json"):

    notes = load_notes(filename)
    new_id = notes[-1]['id'] + 1 if notes else 1
    new_note = {"id": new_id, "text": text}
    notes.append(new_note)
    save_notes(notes, filename)
    print(f"Note added successfully with ID: {new_id}")

def delete_note(note_id, filename="notes.json"):

    notes = load_notes(filename)
    
    notes_to_keep = [note for note in notes if note['id'] != note_id]

    if len(notes_to_keep) == len(notes):
        
        print(f"Error: No note found with ID {note_id}.")
    else:
        save_notes(notes_to_keep, filename)
        print(f"Note with ID {note_id} removed successfully.")

def delete_all_notes(filename="notes.json"):

    save_notes([], filename)
    print("All notes have been deleted.")



def start_interactive_mode():
    try  :
        while 1 :
            print ("Commands:")
            print("1. list: To show all notes.")
            print("2. add: To add a new note.")
            print("3. delete: To delete a note with specified id.")
            print("4. delete-all: To delete all notes.")
            print("5. Exit")

            # option = int(input("Enter no: "))

            try:
                option = int(input("Enter no: "))
            except ValueError:
                print("----------")
                print("Error: Please enter a valid number.")
                print("----------")
                continue


            if option == 1 :
                list_notes()
            elif option == 2:
                note_text = input("Enter the note: ")
                add_note(note_text)
            elif option == 3:
                list_notes()
                id = int(input("Choose note to delete: "))
                delete_note(id)
            elif option == 4:
                confirm = input("Are you sure you want to delete all notes? (Y|Yes): ")
                if confirm.lower() in ['y', 'yes']:
                    delete_all_notes()
            elif option == 5:
                break
            else:
                print("Invalid option")
        
    except Exception as e:
        print (f"Error {e}")

def handle_command_args():
    # if len(sys.argv) < 2:
    #     print("Usage: python notes.py [command] [options]")
    #     print("Commands: list, add, delete, delete-all , help")
    #     sys.exit(1) 

    command = sys.argv[1]

    if command == "list":
        list_notes()
    
    elif command == "help" :
        print("----------")
        print("Usage: python notes.py [command] [options]")
        print("----------")
        print ("Commands:")
        print("list: To show all notes.")
        print("\tcommand: 'python notes.py list'.")

        print("add: To add a new note.")
        print("\tcommand: 'python notes.py add \"the new note here!\"'.")

        print("delete: To delete a note with specified id.")
        print("\tcommand: 'python notes.py delete 1'.")

        print("delete-all: To delete all notes.")
        print("\tcommand: 'python notes.py delete-all'.")

    
    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide the text for the note.")
            print("Example: python notes.py add \"My new note text\"")
        else:
            note_text = " ".join(sys.argv[2:])
            add_note(note_text)
            
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Please provide the ID of the note to delete.")
            print("Example: python notes.py delete 5")
        else:
            try:
                note_id_to_delete = int(sys.argv[2])
                delete_note(note_id_to_delete)
            except ValueError:
                print("Error: The ID must be a number.")

    elif command == "delete-all":
        confirmation = input("Are you sure you want to delete ALL notes? This cannot be undone. (yes/no): ")
        if confirmation.lower() == 'yes':
            delete_all_notes()
        else:
            print("Operation cancelled.")
            
    else:
        print(f"Error: Unknown command '{command}'")
        print("Available commands: list, add, delete, delete-all")

if __name__ == "__main__":


    if len(sys.argv) < 2:
        start_interactive_mode()

    else: 
        handle_command_args()