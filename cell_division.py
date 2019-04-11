# CS241_Week9E_Solved

import random

class Cell:
    
    def __init__(self):
        self.id = random.randint(0,10000)
        self.name = "Cell"
    
    def divide(self):
        return Cell()
        
    def display(self):
        print("{}-{}" .format(self.name, self.id))

def main():
    cells = [Cell()]
    while True:
        print("Number of cells: {}" .format(len(cells)))
        for cell in cells:
            cell.display()
            
        input("Press Enter to Divide Again.")
        
        new_cells = []
        # Call divide for each cell
        # Add the new cells into a seperate list
        # Should not modify the list that we are iterating through
        for cell in cells:
            #cells.append(cell.divide())
            new_cells.append(cell.divide())
        cells += new_cells

        # Another option: 
        # Option 1: Loop through a copy of the list using the copy library
        #
        # for cell in copy.copy(cells):
        #
        # Option 2: Use slicing (we haven't learned this one in class yet)
        #
        # for cell in cells[:]:
        
if __name__ == "__main__":
    main()