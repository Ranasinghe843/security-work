# Homework Number:  03
# Name:             Samitha Ranasinghe
# ECN Login:        sranasi
# Due Date:         02/02/2023

import sys

def multiply(a,b):
    # Arguments:
    # * a: first number to be multiplied
    # * b: second number to be multiplied
    # Function Description:
        # This function returns the multiplication of two integers
        # through bitwise operation and addition

    res = 0
    if b < 0:
        if a < 0:
            a = abs(a)
            b = abs(b)
        else:
            a, b = b, a
    while b > 0:
        if (b & 1):
            res += a
        
        a = a << 1
        b = b >> 1
    
    return res

def quotient(a,b):
    # Arguments:
    # * a: number to be divided from
    # * b: number to be divided with
    # Function Description:
        # This function was modified from a function that
        # only worked with positive numbers and tweaked to
        # work with negative numbers as well
    ans = 0
    if ((a < 0) & (b >= 0)) | ((a >= 0) & (b < 0)):
        neg = 1
    else:
        neg = 0

    a = abs(a)
    b = abs(b)

    for ind in range(31,-1,-1):

        if b << ind <= a  :
            a -= b << ind
            ans += 1 << ind

    if neg:
        ans = multiply(ans, -1) - 1
    
    return ans

def MI(num, mod):
    # Arguments:
    # * num: the integer the MI is found for
    # * mod: the integer prouding sey 
    # Function Description:
        # This function uses ordinary integer arithmetic implementation
        # of the Extended Euclid's Algorithm to find the MI of the
        # first-arg integer vis-a-vis the second-arg integer.
    # Function is borrowed from lecture 5
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = quotient(num, mod)
        num, mod = mod, num % mod
        x, x_old = x_old - multiply(q, x), x
        y, y_old = y_old - multiply(q, y), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))

if __name__ == "__main__":

    if len(sys.argv) != 3:  
        sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0]) 
        sys.exit(1) 

    NUM, MOD = int(sys.argv[1]), int(sys.argv[2])

    MI(NUM, MOD)
    