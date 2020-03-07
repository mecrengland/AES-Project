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
    for i in range(0, int(math.ceil(len(binaryPlainText)/128))):
        listOfBlocks.append(TransformToStateArray(binaryPlainText[i*128:(i+1)*128]))
        
        # State array test print
        print("Block " + str(i) + ": ")
        print(listOfBlocks[i])
        print('\n')
        
    # State array test print
    print(keyStateArray)
    print('\n')
    
    # Key Addition
    xorOutput = KeyAddition(listOfBlocks[0], keyStateArray)
    print(xorOutput)
    
    # 10 Rounds of AES
    for i in range(0,2):
        # Print round number
        print("Round: " + str(int(i+1)))
        
        # Byte Substitution - must convert to hex
        hexOutput = BinaryToHex(xorOutput)
        print(hexOutput)
        byteSubstitution = ByteSubstitution(hexOutput)
        print(byteSubstitution)
        
        # Shift Rows
        
        # Mix Column
        
        # Key Addition - must convert back to binary
        binaryValues = HexToBinary(byteSubstitution)
        xorOutput = KeyAddition(binaryValues, keyStateArray)
        print(xorOutput)
    
def DecryptAES(cipherText, key):
    
    if(not(len(key) == 128)):
        print("INVLAID KEY LENGTH, PLEASE TRY AGAIN")
        exit
        
def BinaryToHex(inputString):
    for i in range(len(inputString)):
        for j in range(len(inputString[i])):
            decimalValue = int(inputString[i][j], 2)
            inputString[i][j] = str(hex(decimalValue)[2:])
            while(len(inputString[i][j]) < 2):
                inputString[i][j] = "0" + inputString[i][j] 
    
    return inputString  

def HexToBinary(inputString):      
    scale = 16
    
    for i in range(len(inputString)):
        for j in range(len(inputString[i])):            
            inputString[i][j] = str((bin(int(inputString[i][j], scale)))[2:] )
            while(len(inputString[i][j]) < 8):
                inputString[i][j] = "0" + inputString[i][j]  
    
    return inputString          

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
    for i in range(0, int(math.ceil(len(inputBytes)/8))):
        
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

"""
Receives 16 bytes and XORs with 16 byte key.
""" 
def KeyAddition(stateArray, key):
    
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
Receives 16 bytes and substitutes with sBox value.
""" 
def ByteSubstitution(hexStateArray):
    xValue = ""
    yValue = ""
    
    sBox = [["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
             ["CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"],
             ["B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15"],
             ["04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75"],
             ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84"],
             ["53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"],
             ["D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8"],
             ["51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"],
             ["CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73"],
             ["60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"],
             ["E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79"],
             ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08"],
             ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"],
             ["70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E"],
             ["E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF"],
             ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]]
     
     
     
    for i in range(len(hexStateArray)):
        for j in range(len(hexStateArray[i])):
             iteration = 0
             
             tempVal = hexStateArray[i][j]
             
             for k in tempVal:                  
                 if(k == "A" or k == "a"):
                     k = "10"
                 elif(k == "B" or k == "b"):
                     k = "11"
                 elif(k == "C" or k == "c"):
                     k = "12"
                 elif(k == "D" or k == "d"):
                     k = "13"
                 elif(k == "E" or k == "e"):
                     k = "14"
                 elif(k == "F" or k == "f"):
                     k = "15"
                 
                 if(iteration == 0):
                     xValue = int(k)
                 else:
                     yValue = int(k)
                     hexStateArray[i][j] = sBox[xValue][yValue]
                     
                 iteration += 1       
             
    return hexStateArray      
  
"""    
def ShiftRows():
    print("null")
    
def MixColumns():
    print("null")
    
def AddRoundKey():
    print("null")
    
def InvMixColumns():
    print("null")
    
def InvByteSubstitution():
    print("null")
    
def RotWord():
    print("null")
    
def SubWord():
    print("null")
"""