from abc import ABC
from abc import abstractmethod

class Employee(ABC):
    
    def __init__(self):
        self.name = ""
    
    @abstractmethod
    def display(self):
        pass
    
    @abstractmethod
    def get_paycheck(self):
        pass
        
class HourlyEmployee(Employee):
    
    def __init__(self):
        super().__init__()
        self.hourly_wage = 0
        self.hour = 0
        
    def display(self):
        print("{} - ${}/hour".format(self.name, self.hourly_wage))
        
    def get_paycheck(self):
        return self.hour * self.hourly_wage
        
class SalaryEmployee(Employee):
    
    def __init__(self):
        super().__init__()
        self.salary = 0

    def display(self):
        print("{} - ${:.2f}/year".format(self.name, self.salary))
               
    def get_paycheck(self):
        return self.salary/24      
 
def display_employee_data(employee):
        employee.display()
        print("Paycheck: $ {:.2f}.".format(employee.get_paycheck()))
 
def main():
    employees = []
    command = ""
    while command != "q":
        command = input("enter h(hourly employee), s(salary employee) or q to quit: ")
        if command == "h":
            h = HourlyEmployee()
            h.name = input("Enter a name: ")
            h.hourly_wage = int(input("Enter an hourly wage: "))
            h.hour = int(input("Enter your working hours: "))
            employees.append(h)
        if command == "s":
            s = SalaryEmployee()
            s.name = input("Enter a name: ")
            s.salary = int(input("Enter a salary: "))
            employees.append(s)
    for employee in employees:
        display_employee_data(employee)

        
if __name__ == "__main__":
    main()
            
        