# -*- coding: utf-8 -*-
"""
Authors: Megan England & Hogan Myers

Author Notes:
    
Since this AES implementation is only for a key size of 128,
Nk (# of words) will always be 4, and Nr (# of rounds) will 
always be 10.


"""

"""
own test cases:
EncryptAES("0123456789ABCDEF","")
"""

import math

# Global Variables:
Nk = 4
Nr = 10
Nb = 4


def EncryptAES(plainText, key):
    
    '''
    TESTING PURPOSES ONLY
    '''
    for i in range(0,128):
        key += "0";
    
    if(not(len(key) == 128)):
        print("INVLAID KEY LENGTH, PLEASE TRY AGAIN")
        exit
        
    keyStateArray = TransformToStateArray(key)
    
    # List of blocks of 16 bytes
    listOfBlocks = []
    # Binary representation of plain text
    binaryPlainText = ""
    
    # To allow for proper state array transformation, end is padded with spaces 
    while(len(plainText)%16 != 0):
        plainText += " "
    
    # Convert plain text to binary
    for character in plainText:
        tempBinary = str(bin(ord(character))[2:])
            
        while(len(tempBinary) < 8):
            tempBinary = "0" + tempBinary
        
        binaryPlainText += tempBinary
    
    # For each block of 16 bytes, place into state array and add to list of blocks
    for i in range(0, math.ceil(len(binaryPlainText)/128)):
        listOfBlocks.append(TransformToStateArray(binaryPlainText[i*128:(i+1)*128]))
        
        
        # State array test print
        print("Block " + str(i) + ": ")
        print(listOfBlocks[i])
        print('\n')
        
    # State array test print
    print(keyStateArray)
    print('\n')
    
    print(XorBits(listOfBlocks[0], keyStateArray))
        
    
def DecryptAES(cipherText, key):
    
    if(not(len(key) == 128)):
        print("INVLAID KEY LENGTH, PLEASE TRY AGAIN")
        exit

"""
Receives 16 bytes and returns them in a state array corresponding to AES
standard.
"""  
def TransformToStateArray(inputBytes):
    
    row0 = []
    row1 = []
    row2 = []
    row3 = []
    
    # Places bytes in corresponding rows of state array
    for i in range(0, math.ceil(len(inputBytes)/8)):
        
        byteToAdd = inputBytes[i*8:(i+1)*8]
        
        if(i%4 == 0):
            row0.append(byteToAdd)
        elif(i%4 == 1):
            row1.append(byteToAdd)
        elif(i%4 == 2):
            row2.append(byteToAdd)
        elif(i%4 == 3):
            row3.append(byteToAdd)
        
    return [row0, row1, row2, row3]

def XorBits(stateArray, key):
    
    for i in range(0, 4):        
        for j in range(0, 4):
            for k in range(0, len(stateArray[i][j])):
                # Changing stateArray[i][j] at location k in string
                if (stateArray[i][j][k] == key[i][j][k]):
                    stateArray[i][j] = stateArray[i][j][:k] + "0" + stateArray[i][j][k+1:]
                else:
                    stateArray[i][j] = stateArray[i][j][:k] + "1" + stateArray[i][j][k+1:]
    
    return stateArray
        
"""
def RoundByteTransform(inputBlock):
    
    # Initial round key addition
    AddRoundKey()
    
    # First Nr-1 rounds
    for i in range(0,Nr-1):
        SubBytes()
        ShiftRows()
        MixColumns
        AddRoundKey()
    
    SubBytes()
    ShiftRows()
    AddRoundKey()
        
    
    return inputBlock

def SubBytes():
    print("null")
    
def ShiftRows():
    print("null")
    
def MixColumns():
    print("null")
    
def AddRoundKey():
    print("null")
    

    
def InvMixColumns():
    print("null")
    
def InvSubBytes():
    print("null")
    
def RotWord():
    print("null")
    
def SubWord():
    print("null")
"""