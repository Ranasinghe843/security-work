# Homework Number:  06
# Name:             Samitha Ranasinghe
# ECN Login:        sranasi
# Due Date:         02/28/2023

import sys
from BitVector import *
import PrimeGenerator
from solve_pRoot import solve_pRoot

e = 3

def generate():
    generator = PrimeGenerator.PrimeGenerator(bits = 128)
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
    
    return p, q

def encrypt():
    write_files = [sys.argv[3], sys.argv[4], sys.argv[5]]
    n = []
    for i in range(3):
        p, q = generate()
        n.append(p * q)
        message = BitVector(filename = sys.argv[2])
        FILEOUT = open(write_files[i], 'w')
        while (message.more_to_read):
            bv = message.read_bits_from_file( 128 )
            if bv.size < 128:
                bv.pad_from_right(128 - bv.size)
            bv.pad_from_left(128)

            enc_bv = BitVector(intVal = pow(int(bv), e, n[i]), size = 256)

            FILEOUT.write(enc_bv.get_bitvector_in_hex())

        FILEOUT.close()
        message.close_file_object()
    
    with open(sys.argv[6], 'w') as fptr:
        fptr.write(str(n[0]))
        fptr.write('\n')
        fptr.write(str(n[1]))
        fptr.write('\n')
        fptr.write(str(n[2]))

def crack():
    n_str = open(sys.argv[5]).read().splitlines()
    n = [int(x) for x in n_str]
    n_bv = [BitVector(intVal = x) for x in n]

    enc_bv = []

    for i in range(2, 5):
        FILEIN = open(sys.argv[i], 'r')
        hex_string = FILEIN.read()
        FILEIN.close()
        enc_bv.append(BitVector(hexstring = hex_string))

    FILEOUT = open(sys.argv[6], 'w')
    for i in range(0, len(enc_bv[0]) // 256):
        bv = [x[i*256:(i+1)*256] for x in enc_bv]

        Ni = [(n[1]*n[2]), (n[0]*n[2]), (n[0]*n[1])]
        Ni_bv = [BitVector(intVal = x) for x in Ni]

        xi = [y.multiplicative_inverse(x) for x,y in zip(n_bv, Ni_bv)]

        crt_sum = [int(x)*y*int(z) for x, y, z, in zip(bv, Ni, xi)]

        decrypted = BitVector(intVal=solve_pRoot(3, pow(sum(crt_sum), 1, n[0]*n[1]*n[2])), size=256)

        pad, message = decrypted.divide_into_two()
        FILEOUT.write(message.get_bitvector_in_ascii())
    FILEOUT.close()

if __name__ == "__main__":

    if sys.argv[1] == "-e":
        encrypt()
    
    if sys.argv[1] == "-c":
        crack()