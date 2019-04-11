class BalanceError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class OutOfChecksError(Exception):
    def __init__(self,  message):
        super().__init__(message)       
        
    

class CheckingAccount:
    
    def __init__(self, starting_balance, num_checks):
        if starting_balance < 0:
            raise BalanceError("Balance cannot be negative")
        if num_checks <= 0:
            raise OutOfChecksError("Insufficient number of checks")
        self.balance = starting_balance
        self.check_count = num_checks

                    
    def deposit(self, amount):
        if amount < 0:
            raise ValueError
        self.balance += amount
        
    def write_check(self, amount):
        if amount < 0:
            raise ValueError
        if self.balance < 0:
            raise BalanceError("Balance cannot be negative")
        if self.check_count <= 0:
            raise OutOfChecksError("Out of check")
        
        self.balance -= amount
        
        self.check_count -= 1
        
    def display(self):
        print("Balance: {:.2f}, The number of check: {}".format(self.balance, self.check_count))
        
    def apply_for_credit(self, amount):
        pass

def display_menu():
    """
    Displays the available commands.
    """
    print()
    print("Commands:")
    print("  quit - Quit")
    print("  new - Create new account")
    print("  display - Display account information")
    print("  deposit - Desposit money")
    print("  check - Write a check")


def main():
    """
    Used to test the CheckingAccount class.
    """
    acc = None
    command = ""

    while command != "quit":
        display_menu()
        command = input("Enter a command: ")

        if command == "new":
            try:
                balance = float(input("Starting balance: "))
                num_checks = int(input("Numbers of checks: "))
                acc = CheckingAccount(balance, num_checks)
            except ValueError as e:
                print(e)                
            except BalanceError as e:
                print(e)
            except OutOfChecksError as e:
                print(e)
        elif command == "display":
            acc.display()
        elif command == "deposit":
            amount = float(input("Amount: "))
            acc.deposit(amount)
        elif command == "check":
            try:
                amount = float(input("Amount: "))
                acc.write_check(amount)
            except ValueError as e:
                print(e)  
            except BalanceError as e:
                print(e)
            except OutOfChecksError as e:
                print(e)
        elif command == "credit":
            amount = float(input("Amount: "))
            acc.apply_for_credit(amount)


if __name__ == "__main__":
    main()
        