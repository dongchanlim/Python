"""
File: ta10-solution.py
Author: Br. Burton
This file demonstrates the merge sort algorithm. There
are efficiencies that could be added, but this approach is
made to demonstrate clarity.
"""

from random import randint
MAX_NUM = 100


def merge_sort(items):
    """
    Sorts the items in the list
    :param items: The list to sort
    """
    
    if len(items) <= 1:
        return
    
    mid = len(items) // 2
    left_list = items[:mid]
    right_list = items[mid:]
    

    merge_sort(left_list)
    merge_sort(right_list)
    
    i = 0
    j = 0
    k = 0
    
    while i < len(left_list)  and j < len(right_list) :
        if left_list[i] < right_list[j]:
            items[k] = left_list[i]
            i += 1
            k += 1
        else:
            items[k] = right_list[j]
            j += 1
            k += 1


    while i < len(left_list):
        items[k] = left_list[i]
        i += 1
        k += 1



    while j < len(right_list):
        items[k] = right_list[j]
        j += 1
        k += 1
        


def generate_list(size):
    """
    Generates a list of random numbers.
    """
    items = [randint(0, MAX_NUM) for i in range(size)]
    return items


def display_list(items):
    """
    Displays a list
    """
    for item in items:
        print(item)


def main():
    """
    Tests the merge sort
    """
    size = int(input("Enter size: "))

    items = generate_list(size)
    print(items)
    merge_sort(items)

    print("\nThe Sorted list is:")
    display_list(items)


if __name__ == "__main__":
    main()



    