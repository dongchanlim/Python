# CS241_Week10A_Solved

def sort(numbers):
    # Algorithim for Bubble Sort for a list of size n
    # Pass 1: Move the largest number into position n-1 by swapping numbers starting at position 0
    # Pass 2: Move the second largest number into position n-2 by swapping numbers starting at position 0 
    # ...
    # Pass n-1: Move the second smallest number into position 1 by swapping numbers at position 0 and 1
    # The smallest number will be left in position 0.

    # Complete passes by looping from n-1 to 1 decreasing.
    for sort_pos in range(len(numbers)-1, 0, -1):
       # Consider swapping each pair starting from 0 to sort_pos-1
       # This will result in compairing positions 0 and 1, 1 and 2, sort_pos-1 and sort_pos
       for swap_pos in range(sort_pos):
          # Compare swap_pos and swap_pos+1
          if numbers[swap_pos] > numbers[swap_pos+1]:
             # Swap if needed
             # Note the syntax for swapping in python ... very convienant.
             numbers[swap_pos], numbers[swap_pos+1] = numbers[swap_pos+1], numbers[swap_pos]

def main():
    numbers = [5, 3, 1, 7, 9, 5, 8, 7, 6, 2, 4, 3, 1, 6, 3, 8, 9, 4, 5, 3]
    sort(numbers)
    print(numbers)

if __name__ == "__main__":
    main()
