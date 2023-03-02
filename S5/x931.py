# Homework Number:  05
# Name:             Samitha Ranasinghe
# ECN Login:        sranasi
# Due Date:         02/21/2023

import sys
from BitVector import *

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []

mix_col_mat = [ [2, 3, 1, 1],
                [1, 2, 3, 1],
                [1, 1, 2, 3],
                [3, 1, 1, 2]]

def genTables():
    # Arguments:
    # None
    # Function Description:
        # Computes the Lookup tables for the byte substition step
        # in AES. The lookup tables for both encrytion and
        # decryption is produced

    # Code was borrowed from Lecture 8 notes
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))

def get_round_keys(key_file):
    # Arguments:
    # None
    # Function Description:
        # Obtains the key from the file as a textstring and
        # calls gen_key_schedule function to obtain list of
        # 60 keywords. It then combines them to produce 15
        # round keys

    # Code was tweaked from Lecture 8 notes
    key_bv = BitVector(textstring=open(key_file, "r").read())
    key_words = gen_key_schedule(key_bv)
    round_keys = [None for i in range(15)]
    for i in range(15):
        round_keys[i] = key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3]
    return(round_keys)

def gen_key_schedule(key_bv):
    # Arguments:
    # * key_bv: BitVector containing key
    # Function Description:
        # Receives the key and produces a list of 60 key
        # words for the 15 round keys at 4 key words each

    # Code was borrowed from Lecture 8 notes
    byte_sub_table = gen_subbytes_table()
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

def gee(keyword, round_constant, byte_sub_table):
    
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

def sub_bytes(state):
    # Arguments:
    # * state: BitVector containing block to be byte substituted
    # Function Description:
        # When the 128 block is sent to be byte substituted, 8 bits
        # are taken at a time and then used as the index for the
        # table produced. The value as the index is then put into
        # the block as the substituted value after padding.
    for i in range(16):
        subbyte = state[i*8:(i+1)*8].int_val()
        state[i*8:(i+1)*8] = BitVector(bitstring = format(subBytesTable[subbyte], 'b').zfill(8))

    return state

def conv_to_array(bitstring):
    # Arguments:
    # * bitstring: BitVector containing block to be converted to state array
    # Function Description:
        # Takes in a 128 bit/16 byte string of bits and creates a 4x4 array
        # of BitVectors
    array = [[0 for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            array[j][i] = bitstring[8*j+32*i:8*j+32*i+8]
    return array

def conv_to_list(array):
    # Arguments:
    # * array: 4x4 state array of BitVectors
    # Function Description:
        # Converts the 4x4 array of BitVectors into a single string BitVector
    bitstring = BitVector(size = 128)
    for i in range(4):
        for j in range(4):
            bitstring[8*j+32*i:8*j+32*i+8] = array[j][i]
    return bitstring

def shift_rows(state):
    # Arguments:
    # * state: BitVector containing block to be row shifted
    # Function Description:
        # Shifts Rows for AES implementation
    state = conv_to_array(state)

    out_array = [   [state[0][0], state[0][1], state[0][2], state[0][3]],
                    [state[1][1], state[1][2], state[1][3], state[1][0]],
                    [state[2][2], state[2][3], state[2][0], state[2][1]],
                    [state[3][3], state[3][0], state[3][1], state[3][2]]]

    state = conv_to_list(out_array)

    return state

def matrix_multiply(mat1, mat2):
    # Arguments:
    # * mat1: First matrix to be multiplied
    # * mat2: Second matrix to be multiplied
    # Function Description:
        # Produces the multiplication of 2 matrices where for multiuplication,
        # the GF modular multiplication is used.
    result = [[BitVector(size=8) for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] ^= mat1[i][k].gf_multiply_modular( mat2[k][j] , AES_modulus, 8)

    return result


def mix_columns(state):
    # Arguments:
    # * state: BitVector containing block to be column mixed
    # Function Description:
        # Produces a column mixed block where it is first converted to a state array
        # and then muliplied with the matrix provided to produce column mixed array
        # which is then converted back to a string and returned
    state = conv_to_array(state)
    
    mul_mat = [[BitVector(intVal = mix_col_mat[j][i]) for i in range(4)] for j in range(4)]
    
    state = matrix_multiply(mul_mat, state)

    state = conv_to_list(state)

    return state

def encrypt(round_keys, state):
    # Arguments:
    # * round_keys: list of round keys for encryption
    # * state: BitVector to be encrypted
    # Function Description:
        # Encrypts the content in the specified file using AES and
        # writes the encrypted data into another file.
    state ^= round_keys[0]
    
    for i in range(1, 15):
        state = sub_bytes(state)
        state = shift_rows(state)
        if i != 14:
            state = mix_columns(state)
        state = state ^ round_keys[i]

    return state

def x931(v0, dt, totalNum, key_file):
    """
    * Arguments:
    v0:      128-bit BitVector object containing the seed value
    dt:      128-bit BitVector object symbolizing the date and time
    totalNum: The total number of random numbers to generate
    key_file: Filename for text file containing the ASCII encryption key for AES
    * Function Description:
    This function uses the arguments with the X9.31 algorithm to generate totalNum
        random numbers as BitVector objects.
    Returns a list of BitVector objects, with each BitVector object representing a
        random number generated from X9.31.
    """

    genTables()

    vj = v0
    rj = []
    round_keys = get_round_keys(key_file)

    dt_ede = encrypt(round_keys, dt)

    for _ in range(totalNum):
        rj_now = encrypt(round_keys, vj^dt_ede)
        vj = encrypt(round_keys, rj_now^dt_ede)
        rj.append(rj_now)

    return rj