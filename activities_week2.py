def act_1():
    score = input("what is your score? ").strip()

    # Introduce error handling and recursion to
    # allow the user to mess up without a program crash
    try:
        score = int(score)
    except:
        print("bad number, try again!")
        return act_1()

    if score < 60:
        print("you failed...")
    else:
        print("you passed!")

def act_2():
    temp = input("what is the temperature? ").strip()

    # Introduce error handling and recursion to
    # allow the user to mess up without a program crash
    try:
        temp = int(temp)
    except:
        print("bad number, try again!")
        return act_2()

    if temp > 0:
        print("above freezing")
    elif temp == 0:
        print("freezing")
    else:
        print("below freezing")

def act_4():
    day, month, *_ = input("Input the day and the month, space separated ").strip().lower()
    month = int(month)
    day = int(day)

    if month not in range(1, 12+1): # Python's ranges are exclusive
        print("invalid month")
        # Recurse to let the user try again, and if the month is valid eventually it
        # will simply return from the current function and trigger a chain.
        return act_4()

    if day not in range(1,31+1): # Python's ranges are exclusive
        print("invalid day")
        return act_4()

    if day == 25 and month == 12:
        print("hooray it's xmas day!")
    elif month == 12 and day < 25:
        print("xmas is just around the corner...")
    else:
        print("you still have a long time to wait till xmas...")

def act_5():
    num = input("enter a number: ").strip()

    try:
        num = int(num)
    except ValueError:
        print("invalid number, try again")
        return act_5()

    if num % 2 == 0:
        print("number is even")
    else:
        print("number is odd")


ACTIVITIES = {}
ACTIVITIES[1] = act_1
ACTIVITIES[2] = act_2
ACTIVITIES[4] = act_4
ACTIVITIES[5] = act_5

def main():
    try:
        # get all valid entries with a list comprehension
        keys = ", ".join([str(k) for k in ACTIVITIES.keys()])
        
        print(f"Available activities include: {keys}")
        activity = int(input("which activity to run? ").strip())
        return ACTIVITIES[activity]()
    except ValueError:
        print("\033[1m==> bad index, try again!\033[0m")
        return main()
    except KeyError:
        print("\033[1m==> bad index, try again!\033[0m")
        return main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exiting...")
        exit(1)
