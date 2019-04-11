# CS241_Week9A_Solved

try:
    number = int(input("Enter a number: "))
    print("You entered: {}" .format(number))
except ValueError:
    print("You entered an invalid number!!")

print()

a = [1, 2, 3]
number = int(input("Enter an index: "))
try:
    print("Value = {}" .format(a[number]))  
except IndexError as e:
    print(e)

print()

filename = input("Enter a filename: ")
try:
    with open(filename,"r") as file:
        for line in file:
            print(line)         
except FileNotFoundError as error:
    print(error)
    print("Could not find {}" .format(filename))