class BankAccount:
    """ Class definition modeling the behavior of a simple bank account """

    def __init__(self, initial_balance):
        """Creates an account with the given balance."""
        self._acc = initial_balance
        self._nof = 0
        
    def deposit(self, amount):
        """Deposits the amount into the account."""
        print "Deposit", amount
        self._acc += amount 
        
    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance.
        """
        print "Before Withrawal Balance = ", self._acc 
        print "Withraw = ", amount 
        
        if (self._acc - amount) < 0:
            print "Takes it less than 0"
            self._acc -= 5 
            self._acc -= amount 
            self._nof += 1
        else:
            self._acc -= amount
        
        print "After Withrawal Balance = ", self._acc 
            
    def get_balance(self):
        """Returns the current balance in the account."""
        return self._acc
    
    def get_fees(self):
        """Returns the total fees ever deducted from the account."""
        return self._nof*5
    
my_account = BankAccount(10)
my_account.withdraw(15)
my_account.deposit(20)
print my_account.get_balance(), my_account.get_fees()

my_account = BankAccount(10)
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(5)
my_account.withdraw(15)
my_account.deposit(20)
my_account.withdraw(5) 
my_account.deposit(10)
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(30)
my_account.withdraw(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(50) 
my_account.deposit(30)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(10) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(10)
my_account.deposit(20)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
print my_account.get_balance(), my_account.get_fees()