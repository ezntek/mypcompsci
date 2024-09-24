import math

def isprime(n):
    "simple prime brute forcer"

    max = int(math.sqrt(n))
    for num in range(0, max):
        if n % num == 0:
            return False
    return True

# ex 1
filename = input("enter filename: ")
open(filename, "w").close() # no need to save file object to variable as no data must be written

# ex 2
with open("pets.txt", "r") as fp:
    print(fp.read())

# ex 3 
pet_name = input("what is the name of your pet? ")
with open("pets.txt", "a") as fp:
    fp.write(pet_name)

# ex 4
with open("pets.txt", "r") as fp:
    lines = fp.readlines()
    print(f"first: {lines[0]}, last: {lines[len(lines)-1]}")

# ex 5
with open("pets.txt", "r") as fp:
    lines = fp.readlines()
    print(lines)

# ex 6
with open("pets.txt", "r") as fp:
    lines = fp.readlines()
    longest = 0
    for line in lines:
        if len(line) > longest:
            longest = len(line)
    print(longest)

# ex 7
pet_name = input("what is the name of the pet? ")
with open("pets.txt", "r") as fp:
    lines = fp.readlines()
    if pet_name in lines:
        print("in the file")
    else:
        print("not in file")

# ex 8
with open("pets.txt", "r") as fp:
    lines = fp.readlines()
    for line in lines:
        if line.capitalize() != line:
            print(f"error found at {line}")
            break


# ex 9
with open("scores.txt", "r") as scores_fp:
    scores = scores_fp.readlines()
    scores.reverse()


with open("scores2.txt", "a") as scores2_fp:
    scores2_fp.writelines(scores)

# ex 10
user_score = int(input("enter the desired score: "))

with open("scores.txt", "r") as fp:
    scores = fp.readlines()

for score in scores:
    if int(score) > user_score:
        print(score)

# ex 11
with open("scores.txt", "r") as fp:
    scores = fp.readlines()

with open("new_scores.txt", "a") as fp:
    for score in scores:
        fp.write((score + '\n')*2)

# ex 12
with open("scores.txt", "r") as fp:
    scores = fp.readlines()

for score in scores:
    if isprime(int(score)):
        print(score)
