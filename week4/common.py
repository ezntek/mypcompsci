import subprocess

def err(txt):
    """
    Print text in red and bold to display an error
    """

    # \033[31m is for red, \033[1m is for bold, \033[0m is to reset the color
    print(f"\033[31m\033[1m{txt}\033[0m")

def info(txt):
    """
    Print text in green and bold to display info
    """

    # \033[32m is for green, \033[1m is for bold, \033[0m is to reset the color
    print(f"\033[32m\033[1m{txt}\033[0m")

def clear():
    """
    Clear the screen on a UNIX-like system.
    """

    subprocess.run(["clear"])

def input_int(*args, **kwargs) -> int:
    """
    using input without any inputs might lead to unwanted program crashes.
    with *args and **kwargs and recursion a safe function for inputting numbers
    that will not result in program crashes should be used.

    *args are all the unnamed parameters, and **kwargs are all keyword arguments.
    """

    val = input(*args, **kwargs) # expand out the args and keyword args

    try:
        return int(val)
    except ValueError:
        err("Invalid Input, try again!")
        return input_int(*args, **kwargs)

def yes_no(prompt: str) -> bool:
    """
    Get a yes or no from the user
    """
    try:
        choice = input(prompt).strip().lower()[0]
    except IndexError:
        print("invalid choice")
        return yes_no(prompt)

    return choice == "y"


