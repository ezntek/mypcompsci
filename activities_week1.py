def act_1():
    word = input("what is the word? ").strip()
    print(word.upper())

def act_2():
    name = input("what is your name? ").strip()
    print(f"Hello {name}")

def act_3():
    name = input("enter your full name: ").strip()
    
    try:
        (firstname, lastname) = name.split(' ')
        password = firstname[:3] + lastname[:3]
    except ValueError:    
        password = name[:3]

    print(f"Your password is {password}")

def act_4():
    name = input("what is your name? ").strip()

    try:
        age = int(input("what is your age? ").strip())
    except ValueError:
        print("invalid age, please try again.")
        return act_4()
    
    print(f"hello {name}, you are {age}")

def act_5():
    name = input("what is your full name? ").strip()

    firstname, lastname = name.split(' ')
    firstname = firstname[0].upper() + firstname[1:]
    lastname = lastname[0].upper() + lastname[1:]
    
    print(f"your name is {firstname} {lastname}")

def act_8():
    sentence = input("enter a sentence: ").strip()
    nspaces = 0

    for ch in sentence:
        if ch == ' ':
            nspaces += 1

    print(f"there are {nspaces} spaces in the word.")

ACTIVITIES = {}
ACTIVITIES[1] = act_1
ACTIVITIES[2] = act_2
ACTIVITIES[3] = act_3
ACTIVITIES[4] = act_4
ACTIVITIES[5] = act_5
ACTIVITIES[8] = act_8

def main():
    try:
        activity = int(input("which activity to run? ").strip())
        return ACTIVITIES[activity]()
    except ValueError:
        print("bad index, try again!")
        return main()
    except IndexError:
        print("bad index, try again!")
        return main()

if __name__ == "__main__":
    main()
