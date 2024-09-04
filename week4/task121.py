from .common import *
import time # sleep
import subprocess # run: clear
import os
import json

SLEEPTIME = 1.5
MENUTXT = """
\033[1m
====================
        MENU
====================\033[0m
1) View all names
2) Add a name
3) Edit a name
4) Delete a name
5) Clear all names
6) Save your work
7) Exit the program
"""

class NameManager:
    def __init__(self) -> None:
        self.saved = False
        self.names = []
    
        self.prevnames = []
        if os.path.exists("save.json"):
            with open("save.json", "r") as fp: # file pointer
                names_d = json.load(fp)
                self.names = names_d["names"]


    def view_names(self):
        """
        List out all the names in the list.
        """

        if len(self.names) == 0:
            err("There are no names.")
            return

        info("The names are as follows: ")
        for index, name in enumerate(self.names):
            print(f"{index+1}. \033[1m{name}\033[0m")

    def add_name(self):
        """
        Add a name to the list
        """
        
        name = input("What should the new name be? ")
        self.names.append(name)
        info(f"\"{name}\" added to the list.\n")
        self.view_names()

    def delete_name(self):
        self.view_names()
        index = input_int("Which name to delete? ")
        index -= 1
        
        try:
            oldname = self.names.pop(index)
        except IndexError:
            err(f"Index {index+1} doesn't exist in the list.")
            return

        info(f"Deleted name {oldname}.")
    
    def clear_names(self):
        self.prevnames = self.names
        self.names = []
        info("Names Cleared")

    def edit_name(self):
        self.view_names()

        if len(self.names) == 0:
            return

        index = input_int("Which name to edit? ")
        newname = input("What should the new name be? ")
        index -= 1


        try:
            oldname = self.names[index]
        except IndexError:
            err(f"Index {index+1} doesn't exist in the list.")
            return
        
        self.names[index] = newname
        info(f"Changed {oldname} to {newname}")

    def save(self):
        if self.prevnames == self.names:
            err("There are no changes to save.")
        else:
            names_d = { "names": self.names }
            
            with open("save.json", "w") as fp: # file pointer
                json.dump(names_d, fp)

    def exit(self):
        if self.prevnames == self.names:
            return

        err("You have unsaved changes.")
        if yes_no("Would you like to save? "):
            self.save()
        else:
            return
        
        
def menu() -> int:
    print(MENUTXT)
    option = input_int("Choose an option: ")
    if option not in (1, 2, 3, 4, 5, 6, 7):
        err(f"Option {option} is not valid!")
        subprocess.run(["clear"])
        return menu()
    return option
    

def loop():
    name_manager = NameManager()
    
    OPTIONS = {
        1: name_manager.view_names,
        2: name_manager.add_name,
        3: name_manager.edit_name,
        4: name_manager.delete_name,
        5: name_manager.clear_names,
        6: name_manager.save,
    }


    clear()
    while True:
        clear()
        option = menu()

        if option == 7:
            name_manager.exit()
            break
        else:
            OPTIONS[option]()
            time.sleep(SLEEPTIME)

def main():
    try:
        return loop()
    except KeyboardInterrupt:
        print("exiting...")
        exit(1)

if __name__ == "__main__":
    main()
