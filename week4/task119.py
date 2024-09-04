import random
from .common import * # import everything from the common file

def generate_random_value():
    low = input_int("enter a low value: ")
    high = input_int("enter a high value: ")

    if low > high:
        err("the low value is higher than the high value!")
        return generate_random_value() # recursion

    comp_num = random.randint(low, high)
    return comp_num

def guess():
    print("I am thinking of a number...")
    return input_int("guess what it is: ") # fun fact, return takes expressions as well as identifiers!

def check_loop():
    comp_num = generate_random_value()
    
    while True:
        user_guess = guess()

        if user_guess > comp_num:
            print("too big")
            continue
        elif user_guess < comp_num:
            print("too small")
            continue
        else:
            print("you are correct!")
            break

def main():
    try:
        return check_loop()
    except KeyboardInterrupt:
        # avoid a program crash on ctrl-c
        print("exiting...")
        exit(1)

if __name__ == "__main__":
    main()
        
