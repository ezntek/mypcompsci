# A simple Username/Password system made in class for MYP Comp Sci.
#
# Authored by Eason Qin.
#
# This Source code form is licensed under the Unlicense or placed
# under the Public Domain, whichever is more permissive. 

import getpass # getpass() for secure passsword entry

USERNAMES = {}
ADMINPASS = "supersecretpassword" # default admin password

def register_user():
    # Remove leading and trailing bytes
    username = input("what is your username? ").strip()

    # Check if username is already in the system
    if username in USERNAMES:
        print(f"username \"{username}\" already exists!\n")
        return

    password = getpass.getpass("what is your password? ")
    
    # Put into the hashmap
    USERNAMES[username] = password


def login():
    # Remove leading and trailing bytes
    username = input("what is your username? ").strip()

    # Check if username is already in the system
    if username not in USERNAMES:
        print(f"username \"{username}\" does not exist...\n")
        return

    password = getpass.getpass("what is your password? ")
    
    if USERNAMES[username] == password:
        print("access granted...\n")
    else:
        print("intruder alert! \n")

def admin():
    password = getpass.getpass("what is the admin password? ")

    # Deny access if the password is wrong
    if password != ADMINPASS:
        print("intruder alert!\n")
        return

    # Print all username and password data
    if len(USERNAMES.keys()) == 0:
        print("no user data...")
        return
    
    for key, value in USERNAMES.items():
        print(f"Username {key} has a password \"{value}\"")
    
    # Print a newline.
    print()


def main():
    should_exit = False
    while not should_exit:
        # remove whitespaces and make all lowercase
        nextaction = input("e[x]it the program, [c]reate a new user, log in as [a]dmin, or [l]og in? ").lower().strip()
        
        if len(nextaction) < 1:
            print("invalid command...\n")
            continue

        # only read the first character in case of input errors
        match nextaction[0]:
            case 'x':
                should_exit = True
                continue
            case 'c':
                register_user()
            case 'a':
                admin()
            case 'l':
                login()
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exiting...")
        exit(1)
