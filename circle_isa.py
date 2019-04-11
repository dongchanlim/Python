from point import Point

class Circle(Point):
    def __init__(self):
        super().__init__()
        self.radius = 0.0
        
    def prompt_for_circle(self):
        self.prompt_for_point()
        self.radius = input("Enter radius: ")
        
    def display(self):
        super().display()
        print("Radius: {}".format(self.radius))
        
def main():
    circle = Circle()
    circle.prompt_for_circle()
    circle.display()
    

if __name__ == "__main__":
    main()
    
        
        