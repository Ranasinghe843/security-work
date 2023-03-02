# Homework Number:  01
# Name:             Samitha Ranasinghe
# ECN Login:        sranasi
# Due Date:         01/19/2023

def cryptBreak(ciphertextFile, key_bv):
    # Arguments:
    # * ciphertextFile: String containing file name of the ciphertext
    # * key_bv: 16-bit BitVector for the decryption key
    # Function Description:
        # Attempts to decrypt the ciphertext within ciphertextFile file using
        # key_bv and returns the original plaintext as a string

    # Majority of the core code was borrowed from DecryptForFun.py
    # The code for obtaining the key from user and converting into a bitvector was
    # removed and the BLOCKSIZE changed to 16
    
    PassPhrase = "Hopes and dreams of a million years"                          #(C)

    BLOCKSIZE = 16                                                              #(D)
    numbytes = BLOCKSIZE // 8                                                   #(E)

    # Reduce the passphrase to a bit array of size BLOCKSIZE:
    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
    for i in range(0,len(PassPhrase) // numbytes):                              #(G)
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
        bv_iv ^= BitVector( textstring = textstr )                              #(I)

    # Create a bitvector from the ciphertext hex string:
    FILEIN = open(ciphertextFile)                                               #(J)
    encrypted_bv = BitVector( hexstring = FILEIN.read() )                       #(K)

    # Create a bitvector for storing the decrypted plaintext bit array:
    msg_decrypted_bv = BitVector( size = 0 )                                    #(T)

    # Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv                                            #(U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):                          #(V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]                          #(W)
        temp = bv.deep_copy()                                                   #(X)
        bv ^=  previous_decrypted_block                                         #(Y)
        previous_decrypted_block = temp                                         #(Z)
        bv ^=  key_bv                                                           #(a)
        msg_decrypted_bv += bv                                                  #(b)

    # Extract plaintext from the decrypted bitvector:    
    outputtext = msg_decrypted_bv.get_text_from_bitvector()                     #(c)

    return outputtext


if __name__ == "__main__":

    from BitVector import *

    for i in range(2**16):
        key_bv = BitVector(intVal=i, size=16)
        decryptedMessage = cryptBreak('ciphertext.txt', key_bv)
        if 'Sir Lewis' in decryptedMessage:
            print(i)
            break

    print(decryptedMessage)