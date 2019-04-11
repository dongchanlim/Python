
def main():
  valid_input = False

  while valid_input != True:
    try:
      number = int(input("Enter a number: "))
      print("The result is: {}".format(number * 2))
      valid_input =  True
    except ValueError:
      print("The value entered is not valid")
      
if __name__ == "__main__":
  main()