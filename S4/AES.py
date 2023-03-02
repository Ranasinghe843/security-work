# Homework Number:  04
# Name:             Samitha Ranasinghe
# ECN Login:        sranasi
# Due Date:         02/14/2023

import sys
from BitVector import *

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []
invSubBytesTable = []

mix_col_mat = [ [2, 3, 1, 1],
                [1, 2, 3, 1],
                [1, 1, 2, 3],
                [3, 1, 1, 2]]

inv_mix_col_mat = [ ["E", "B", "D", "9"],
                    ["9", "E", "B", "D"],
                    ["D", "9", "E", "B"],
                    ["B", "D", "9", "E"]]

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
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))



def get_round_keys():
    # Arguments:
    # None
    # Function Description:
        # Obtains the key from the file as a textstring and
        # calls gen_key_schedule function to obtain list of
        # 60 keywords. It then combines them to produce 15
        # round keys

    # Code was tweaked from Lecture 8 notes
    key_bv = BitVector(textstring=open(sys.argv[3], "r").read())
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

    for i in range(16):
        subbyte = state[i*8:(i+1)*8].int_val()
        state[i*8:(i+1)*8] = BitVector(bitstring = format(subBytesTable[subbyte], 'b').zfill(8))

    return state

def inv_sub_bytes(state):

    for i in range(16):
        subbyte = state[i*8:(i+1)*8].int_val()
        state[i*8:(i+1)*8] = BitVector(bitstring = format(invSubBytesTable[subbyte], 'b').zfill(8))

    return state

def conv_to_array(bitstring):

    
    array = [[0 for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            array[j][i] = bitstring[8*j+32*i:8*j+32*i+8]
    return array

def conv_to_list(array):

    bitstring = BitVector(size = 128)
    for i in range(4):
        for j in range(4):
            bitstring[8*j+32*i:8*j+32*i+8] = array[j][i]
    return bitstring

def shift_rows(state):

    state = conv_to_array(state)

    """
    # Shift the second row one byte to the left
    state[1] = state[1][8:] + state[1][:8]

    # Shift the third row two bytes to the left
    state[2] = state[2][16:] + state[2][:16]

    # Shift the fourth row three bytes to the left
    state[3] = state[3][24:] + state[3][:24]
    
    """
    out_array = [   [state[0][0], state[0][1], state[0][2], state[0][3]],
                    [state[1][1], state[1][2], state[1][3], state[1][0]],
                    [state[2][2], state[2][3], state[2][0], state[2][1]],
                    [state[3][3], state[3][0], state[3][1], state[3][2]]]

    state = conv_to_list(out_array)

    return state

def inv_shift_rows(state):

    state = conv_to_array(state)

    out_array = [   [state[0][0], state[0][1], state[0][2], state[0][3]],
                    [state[1][3], state[1][0], state[1][1], state[1][2]],
                    [state[2][2], state[2][3], state[2][0], state[2][1]],
                    [state[3][1], state[3][2], state[3][3], state[3][0]]]

    state = conv_to_list(out_array)

    return state

def matrix_multiply(mat1, mat2):
    result = [[BitVector(size=8) for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] ^= mat1[i][k].gf_multiply_modular( mat2[k][j] , AES_modulus, 8)

    return result


def mix_columns(state):

    state = conv_to_array(state)
    
    mul_mat = [[BitVector(intVal = mix_col_mat[j][i]) for i in range(4)] for j in range(4)]
    
    state = matrix_multiply(mul_mat, state)

    state = conv_to_list(state)

    return state

def inv_mix_columns(state):

    state = conv_to_array(state)
    
    mul_mat = [[BitVector(hexstring = inv_mix_col_mat[j][i]) for i in range(4)] for j in range(4)]
    
    state = matrix_multiply(mul_mat, state)

    state = conv_to_list(state)

    return state

def encrypt():
    # Arguments:
    # None
    # Function Description:
        # Encrypts the content in the specified file using AES and
        # writes the encrypted data into another file.
    round_keys = get_round_keys()
    bv = BitVector(filename = sys.argv[2])
    FILEOUT = open(sys.argv[4], 'w')
    while (bv.more_to_read):
        state = bv.read_bits_from_file( 128 )
        if state.size < 128:
            state.pad_from_right(128 - state.size)
        if state.size > 0:

            state ^= round_keys[0]
            
            for i in range(1, 15):
                state = sub_bytes(state)
                state = shift_rows(state)
                if i != 14:
                    state = mix_columns(state)
                state = state ^ round_keys[i]

            FILEOUT.write(state.get_bitvector_in_hex())

    FILEOUT.close()
    bv.close_file_object()

def decrypt():
    # Arguments:
    # None
    # Function Description:
        # Decrypts the content in the specified file using AES and
        # writes the dercypted data into another file.
    round_keys = get_round_keys()
    round_keys.reverse()
    FILEIN = open(sys.argv[2], 'r')
    hex_string = FILEIN.read();
    FILEIN.close()
    bv = BitVector(hexstring = hex_string)
    FILEOUT = open(sys.argv[4], 'w')
    for i in range(0, len(bv) // 128):
        state = bv[i*128:(i+1)*128]
        state ^= round_keys[0]

        for i in range(1, 15):
            state = inv_shift_rows(state)
            state = inv_sub_bytes(state)
            state = state ^ round_keys[i]
            if i != 14:
                state = inv_mix_columns(state)

        FILEOUT.write(state.get_bitvector_in_ascii())
    FILEOUT.close()

if __name__ == "__main__":

    genTables()

    if sys.argv[1] == "-e":
        encrypt()
    
    if sys.argv[1] == "-d":
        decrypt()