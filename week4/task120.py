import random
from .common import *

MENUTXT = """
1) Addition
2) Subtraction
"""

# Type annotations will be used in this file due to preference
def addition() -> tuple[int, int]:
    first_num = random.randint(5, 20)
    second_num = random.randint(5, 20)
    
    print(f"Please evaluate {first_num} + {second_num}")
    user_guess = input_int("What is the result? ")
    sum = first_num + second_num

    return user_guess, sum    


def subtraction() -> tuple[int, int]:
    first_num = random.randint(25, 50)
    second_num = random.randint(1, 25)
    
    print(f"Please evaluate {first_num} - {second_num}")
    user_guess = input_int("What is the result? ")
    difference = first_num - second_num

    return user_guess, difference    


# hashtable with the keys as the choices
OPTIONS = {
    1: addition,
    2: subtraction
}

def menu_input() -> tuple[int, int]:
    option = input_int("Enter 1 or 2: ")

    try:
        return OPTIONS[option]()
    except KeyError:
        err("you entered an invalid option, try again")
        return menu_input()

def menu():
    print(MENUTXT)
    user_guess, answer = menu_input()
    
    if user_guess == answer:
        print(f"your answer was {user_guess}, and you are correct!")
    else:
        print(f"your answer was {user_guess}, however you are wrong. It really is {answer}...")

def main():
    try:
        return menu()
    except KeyboardInterrupt:
        # avoid a program crash on ctrl-c
        print("exiting...")
        exit(1)

if __name__ == "__main__":
    main()
