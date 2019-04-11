# CS241_Week7C_Solved

def factorial(n):
    if n <= 0:
        return 1
    return n * factorial(n-1)
    
for i in range(10):
    print("{}! = {}" .format(i, factorial(i)))


def fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 1
        
    return fib(n-1) + fib(n-2)
 
for i in range(39):
    print(fib(i))

def fib_norecurse(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    prev = 1
    prev_prev = 1
    for i in range(3,n+1):
        sum = prev + prev_prev
        prev_prev = prev
        prev = sum
    return sum

for i in range(100):
    print(fib_norecurse(i))




    