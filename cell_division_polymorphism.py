# CS241_Week9F_Solved

import random
from abc import ABC
from abc import abstractmethod

class Cell(ABC):
    
    def __init__(self, name):
        self.id = random.randint(0,10000)
        self.name = name
    
    @abstractmethod
    def divide(self):
        pass
        
    def display(self):
        print("{}-{}" .format(self.name,self.id))
        
class NormalCell(Cell):
    
    def __init__(self):
        super().__init__("Normal")
        
    def divide(self):
        return [NormalCell()]
    
class MutatedCell(Cell):
    
    def __init__(self):
        super().__init__("Mutated")
        
    def divide(self):
        return [NormalCell(),MutatedCell()]

def main():
    cells = [NormalCell(),MutatedCell()]
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
            new_cells += cell.divide()
        cells += new_cells
        
if __name__ == "__main__":
    main()