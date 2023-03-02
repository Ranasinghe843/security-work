# Homework Number:  06
# Name:             Samitha Ranasinghe
# ECN Login:        sranasi
# Due Date:         02/28/2023

import sys
from BitVector import *
from PrimeGenerator import PrimeGenerator

e = 65537

def generate():
    # Arguments:
    # None
    # Function Description:
        # Uses the prime number generator to keep generating prime numbers
        # until 2 128 bit numbers are produced which are not equal and
        # the totients should be coprime to e
    generator = PrimeGenerator(bits = 128)
    e_bit = BitVector(intVal = e)
    while True:
        check = 0
        p = generator.findPrime()
        q = generator.findPrime()
        if p == q:
            check += 1
        
        p_bit = BitVector(intVal = (p - 1))
        q_bit = BitVector(intVal = (q - 1))
        
        if int(e_bit.gcd(p_bit)) != 1:
            check += 1
        if int(e_bit.gcd(q_bit)) != 1:
            check += 1
        
        if check == 0:
            break
    
    with open(sys.argv[2], 'w') as fptr:
        fptr.write(str(p))
    
    with open(sys.argv[3], 'w') as fptr:
        fptr.write(str(q))

def encrypt():
    # Arguments:
    # None
    # Function Description:
        # Produces a column mixed block where it is first converted to a state array
        # and then muliplied with the matrix provided to produce column mixed array
        # which is then converted back to a string and returned
    with open(sys.argv[3], 'r') as fptr:
        p = int(fptr.read())
    
    with open(sys.argv[4], 'r') as fptr:
        q = int(fptr.read())
    
    n = p * q
    
    message = BitVector(filename = sys.argv[2])
    FILEOUT = open(sys.argv[5], 'w')
    while (message.more_to_read):
        bv = message.read_bits_from_file( 128 )
        if bv.size < 128:
            bv.pad_from_right(128 - bv.size)
        bv.pad_from_left(128)

        enc_bv = BitVector(intVal = pow(int(bv), e, n), size = 256)

        FILEOUT.write(enc_bv.get_bitvector_in_hex())

    FILEOUT.close()
    message.close_file_object()

def decrypt():
    # Arguments:
    # None
    # Function Description:
        # Produces a column mixed block where it is first converted to a state array
        # and then muliplied with the matrix provided to produce column mixed array
        # which is then converted back to a string and returned
    with open(sys.argv[3], 'r') as fptr:
        p = int(fptr.read())
    
    with open(sys.argv[4], 'r') as fptr:
        q = int(fptr.read())
    
    n = p * q
    totient = BitVector(intVal = (p - 1) * (q - 1))
    e_bv = BitVector(intVal = e)
    p_bv = BitVector(intVal = p)
    q_bv = BitVector(intVal = q)

    d = int(e_bv.multiplicative_inverse(totient))

    print(d)

    FILEIN = open(sys.argv[2], 'r')
    hex_string = FILEIN.read()
    FILEIN.close()
    enc_bv = BitVector(hexstring = hex_string)
    FILEOUT = open(sys.argv[5], 'w')
    for i in range(0, len(enc_bv) // 256):
        bv = enc_bv[i*256:(i+1)*256]

        v_p = pow(int(bv), d, p)
        v_q = pow(int(bv), d, q)

        x_p = q * int(q_bv.multiplicative_inverse(p_bv))
        x_q = p * int(p_bv.multiplicative_inverse(q_bv))

        decrypted = BitVector(intVal=pow((v_p * x_p + v_q * x_q), 1, n), size=256)

        pad, message = decrypted.divide_into_two()

        FILEOUT.write(message.get_bitvector_in_ascii())
    FILEOUT.close()

if __name__ == "__main__":

    if sys.argv[1] == "-e":
        encrypt()
    
    if sys.argv[1] == "-d":
        decrypt()

    if sys.argv[1] == "-g":
        generate()