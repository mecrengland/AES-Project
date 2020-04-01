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
import keySchedule
import polynomialDiv
from keySchedule import XOR
from keySchedule import keySchedule128
from polynomialDiv import polyDivRem
import copy
import imp


# Global Variables:
Nk = 4
Nr = 10
Nb = 4


def EncryptAES(plainText, key):
    imp.reload(keySchedule)
    imp.reload(polynomialDiv)
    
    key = key.split()
    
    if(not(len(key) == 16)):
        print("INVLAID KEY LENGTH, PLEASE TRY AGAIN")
        return -1
    
    expandedKey = keySchedule128(key)
    
    # List of blocks of 16 bytes
    listOfBlocks = []
    # Binary representation of plain text
    binaryPlainText = ""
    
    # Convert plaintext into array
    plainText = plainText.split()
    
    # Convert plain text to binary
    for i in range(len(plainText)):
        plainText[i] = bin(int(plainText[i], 16))[2:]
        while(len(plainText[i]) < 8):
            plainText[i] = "0" + plainText[i]
        binaryPlainText += plainText[i]
    
    # For each block of 16 bytes, place into state array and add to list of blocks
    for i in range(0, int(math.ceil(len(binaryPlainText)/128))):
        listOfBlocks.append(TransformToStateArray(binaryPlainText[i*128:(i+1)*128]))
    
    # Print Round 0
    print("Round 0")
    temp = copy.deepcopy(listOfBlocks[0])
    print("Start of Round: ")
    print(BinaryToHex(temp))
    
    # Key Addition
    keyStateArray = TransformToStateArray("".join(expandedKey[:4]))
    xorOutput = KeyAddition(listOfBlocks[0], keyStateArray)
    
    # 10 Rounds of AES
    for i in range(0,10):
        # Print round number
        print("Round " + str(int(i+1)))
        
        # Byte Substitution
        hexOutput = BinaryToHex(xorOutput)
        print("Start of Round: ")
        print(hexOutput)
        byteSubstitutionOutput = ByteSubstitution(hexOutput)
        print("After Byte Substitution: ")
        print(byteSubstitutionOutput)
        
        # Shift Rows
        shiftValueOutput = ShiftRows(byteSubstitutionOutput)
        print("After Shift Rows: ")
        print(shiftValueOutput)
        
        # Convert to binary for Mix Column operation
        binaryValues = HexToBinary(shiftValueOutput)
        
        # Mix Column
        if(not(i == 9)):
            mixColumnOutput = MixColumns(binaryValues)
            temp = copy.deepcopy(mixColumnOutput)
            print("After Mix Columns: ")
            print(BinaryToHex(temp))
        
        # Key Addition
        keyStateArray = TransformToStateArray("".join(expandedKey[(i+1)*4:(i+1)*4+4]))
        if(not(i == 9)): 
            xorOutput = KeyAddition(mixColumnOutput, keyStateArray)
        else:
            xorOutput = KeyAddition(binaryValues, keyStateArray)  
        
    binaryOutput = BinaryToHex(xorOutput)
    finalOutput = arrayToOutput(binaryOutput)
    print("FINAL ENCRYPTED OUTPUT: " + finalOutput)
    
    
def DecryptAES(cipherText, key):
    imp.reload(keySchedule)
    imp.reload(polynomialDiv)
    
    key = key.split()
    
    if(not(len(key) == 16)):
        print("INVLAID KEY LENGTH, PLEASE TRY AGAIN")
        return -1
    
    expandedKey = keySchedule128(key)
    
    # List of blocks of 16 bytes
    listOfBlocks = []
    # Binary representation of cipher text
    binaryCipherText = ""
    
    # Convert plaintext into array
    cipherText = cipherText.split()
    
    # Convert plain text to binary
    for i in range(len(cipherText)):
        cipherText[i] = bin(int(cipherText[i], 16))[2:]
        while(len(cipherText[i]) < 8):
            cipherText[i] = "0" + cipherText[i]
        binaryCipherText += cipherText[i]
    
    # For each block of 16 bytes, place into state array and add to list of blocks
    for i in range(0, int(math.ceil(len(binaryCipherText)/128))):
        listOfBlocks.append(TransformToStateArray(binaryCipherText[i*128:(i+1)*128]))
    
    byteSubstitutionOutput = [[]]
    
    # Print Round 0
    print("Round 0")
    temp = copy.deepcopy(listOfBlocks[0])
    print("Start of Round: ")
    print(BinaryToHex(temp))
    
    # 10 Rounds of AES
    for i in range(0,10):        
        # Key Addition
        keyStateArray = TransformToStateArray("".join(expandedKey[(10-i)*4:(10-i)*4+4]))
        if(not(i == 0)): 
            # Print round number
            print("Round " + str(int(i)))
            print("Start of Round: ")
            temp = copy.deepcopy(byteSubstitutionOutput)
            print(BinaryToHex(temp))
            
            keyAddOutput = KeyAddition(byteSubstitutionOutput, keyStateArray)
        else:
            keyAddOutput = KeyAddition(listOfBlocks[0], keyStateArray)
        
        print("After Key Addition: ")
        temp = copy.deepcopy(keyAddOutput)
        print(BinaryToHex(temp))
        
        # Mix Column
        if(not(i == 0)):
            mixColumnOutput = InvMixColumns(keyAddOutput)
            print("After Mix Columns: ")
            temp = copy.deepcopy(mixColumnOutput)
            print(BinaryToHex(temp))
        else:
            mixColumnOutput = keyAddOutput
        
        # Shift Rows
        shiftValueOutput = InvShiftRows(mixColumnOutput)
            
        # Byte Substitution
        hexOutput = BinaryToHex(shiftValueOutput)
        print("After Shift Rows: ")
        print(hexOutput)
        
        byteSubstitutionOutput = InvByteSubstitution(hexOutput)
        
        byteSubstitutionOutput = HexToBinary(byteSubstitutionOutput)
        
    
    # Key Addition
    print("Round 10")
    print("Start of Round: ")
    temp = copy.deepcopy(byteSubstitutionOutput)
    print(BinaryToHex(temp))
    keyStateArray = TransformToStateArray("".join(expandedKey[:4]))
    finalValues = KeyAddition(byteSubstitutionOutput, keyStateArray)
    
    # Convert result to string
    binaryOutput = BinaryToHex(finalValues)
    finalOutput = arrayToOutput(binaryOutput)
    print("FINAL DECRYPTED OUTPUT: " + finalOutput)
    
"""
Converts 2d array into output string.
"""
def arrayToOutput(inputArray):    
    width, height = 4, 4
    temp = [[0 for x in range(width)] for y in range(height)] 
    outputString = ""
    
    for i in range(len(inputArray)):
        for j in range(len(inputArray[i])):
            temp[j][i] = inputArray[i][j]
            
    for i in range(len(temp)):
        for j in range(len(temp[i])):
            outputString += temp[i][j]
            outputString += " "

    return outputString        

"""
Converts binary string to hex string.
"""          
def BinaryToHex(inputString):
    for i in range(len(inputString)):
        for j in range(len(inputString[i])):
            decimalValue = int(inputString[i][j], 2)
            inputString[i][j] = str(hex(decimalValue)[2:])
            while(len(inputString[i][j]) < 2):
                inputString[i][j] = "0" + inputString[i][j] 
    
    return inputString  

"""
Converts hex string to binary string.
"""  
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
Receives 16 bytes and shifts rows.
"""   
def ShiftRows(hexStateArray):
    width, height = 4, 4
    newHexStateArray = [[0 for x in range(width)] for y in range(height)] 
    
    # row 1 doesn't change
    newHexStateArray[0][0] = hexStateArray[0][0]
    newHexStateArray[0][1] = hexStateArray[0][1]
    newHexStateArray[0][2] = hexStateArray[0][2]
    newHexStateArray[0][3] = hexStateArray[0][3]
    
    # shift 2nd row left by one
    newHexStateArray[1][0] = hexStateArray[1][1]
    newHexStateArray[1][1] = hexStateArray[1][2]
    newHexStateArray[1][2] = hexStateArray[1][3]
    newHexStateArray[1][3] = hexStateArray[1][0]
    
    
    # shift 3rd row left by two
    newHexStateArray[2][0] = hexStateArray[2][2]
    newHexStateArray[2][1] = hexStateArray[2][3]
    newHexStateArray[2][2] = hexStateArray[2][0]
    newHexStateArray[2][3] = hexStateArray[2][1]
    
    # shift 4th row left by 3
    newHexStateArray[3][0] = hexStateArray[3][3]
    newHexStateArray[3][1] = hexStateArray[3][0]
    newHexStateArray[3][2] = hexStateArray[3][1]
    newHexStateArray[3][3] = hexStateArray[3][2]            
    
    return newHexStateArray
    
"""
Receives 16 bytes and multiples columns.
"""   
def MixColumns(hexStateArray):
    constantMatrix = [["00000010", "00000011", "00000001", "00000001"],
                      ["00000001", "00000010", "00000011", "00000001"],
                      ["00000001", "00000001", "00000010", "00000011"],
                      ["00000011", "00000001", "00000001", "00000010"]]
    

    for i in range(0,4):
        
        # Temporary vector to grab the 4 used values for the multiplication
        tempVector = [hexStateArray[0][i], hexStateArray[1][i], hexStateArray[2][i], hexStateArray[3][i]]
        
        for j in range(4):
            
            # Temporary vector holding the 4 used constants from the matrix
            tempVectorConst = [constantMatrix[j][0], constantMatrix[j][1], constantMatrix[j][2], constantMatrix[j][3]]
            # Starting point for 3 XOR operations combining the multiplications
            prevResult = "00000000"
            
            for k in range(4):
                
                if(tempVectorConst[k] == "00000010" or tempVectorConst[k] == "00000011"):
                    
                    # const is 2, GF polynomiol is x, i.e. shift all left 1 bit
                    leftShift = tempVector[k] + "0"
                    
                    # if degree is 8, must reduce
                    if(leftShift[0] == "1"):
                        leftShift = XOR(leftShift[1:], "00011011")
                    else:
                        leftShift = leftShift[1:]
                    
                    if(tempVectorConst[k] == "00000011"):
                        prevResult = XOR(prevResult, XOR(leftShift, tempVector[k]))
                    else:
                        prevResult = XOR(prevResult, leftShift)
                    
                else:
                    # Identity matrix, no change (const is 1)
                    prevResult = XOR(prevResult, tempVector[k])
                    
            hexStateArray[j][i] = prevResult
        
    return hexStateArray


"""
Receives 16 bytes and multiples columns.
"""   
def InvMixColumns(hexStateArray):
    
    constantMatrix = [["00001110", "00001011", "00001101", "00001001"],
                      ["00001001", "00001110", "00001011", "00001101"],
                      ["00001101", "00001001", "00001110", "00001011"],
                      ["00001011", "00001101", "00001001", "00001110"]]    

    for i in range(0,4):
        
        # Temporary vector to grab the 4 used values for the multiplication
        tempVector = [hexStateArray[0][i], hexStateArray[1][i], hexStateArray[2][i], hexStateArray[3][i]]
        
        for j in range(4):
            
            # Temporary vector holding the 4 used constants from the matrix
            tempVectorConst = [constantMatrix[j][0], constantMatrix[j][1], constantMatrix[j][2], constantMatrix[j][3]]
            # Starting point for 3 XOR operations combining the multiplications
            prevResult = "00000000"
            
            for k in range(4):
                
                # Mult by x^3 + x^2 + x
                if(tempVectorConst[k] == "00001110"):
                    result = polyMultWithReduction("00001110", tempVector[k])
                # Mult by x^3 + x + 1
                elif(tempVectorConst[k] == "00001011"):
                    result = polyMultWithReduction("00001011", tempVector[k])
                # Mult by x^3 + x^2 + 1
                elif(tempVectorConst[k] == "00001101"):
                    result = polyMultWithReduction("00001101", tempVector[k])
                # Mult by x^3 + 1
                elif(tempVectorConst[k] == "00001001"):
                    result = polyMultWithReduction("00001001", tempVector[k])
                
                prevResult = XOR(prevResult, result)
                    
            hexStateArray[j][i] = prevResult
        
    return hexStateArray

# Multiplies two polynomials and returns them as a binary string
def polyMultWithReduction(poly1, poly2):
    
    # Irreducible polynomial from AES
    px = [1,0,0,0,1,1,0,1,1]
    # Empty arrays to hold data
    resultArr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    # Multiplies all non-zero coefficient elements in polynomial
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            if(poly1[i] == "1" and poly2[j] == "1"):
                if(resultArr[i + j] == 0):
                    resultArr[i + j] = 1
                else:
                    resultArr[i + j] = 0

    # Divide the result by P(x) and obtain the remainder... i.e. the mod
    resultArr = polyDivRem(resultArr, px)
    
    # If numpy does weird stuff this fixes it
    for i in range(len(resultArr)):
        if(resultArr[i] == -1 or resultArr[i] == 1):
            resultArr[i] = "1"
        else:
            resultArr[i] = "0"
            
    # Pad array with 0's to make sure it is still 8 bits
    while(len(resultArr) < 8):
        resultArr.insert(0,"0")
    # Remove extra zeros if needed
    while(len(resultArr) > 8):
        del resultArr[0]
    
    return "".join(resultArr)


"""
Receives 16 bytes and substitutes with sBox value.
"""            
def InvByteSubstitution(hexStateArray):
    xValue = ""
    yValue = ""
    
    sBox = [["52", "09", "6A", "D5", "30", "36", "A5", "38", "BF", "40", "A3", "9E", "81", "F3", "D7", "FB"],
                ["7C", "E3", "39", "82", "9B", "2F", "FF", "87", "34", "8E", "43", "44", "C4", "DE", "E9", "CB"],
                ["54", "7B", "94", "32", "A6", "C2", "23", "3D", "EE", "4C", "95", "0B", "42", "FA", "C3", "4E"],
                ["08", "2E", "A1", "66", "28", "D9", "24", "B2", "76", "5B", "A2", "49", "6D", "8B", "D1", "25"],
                ["72", "F8", "F6", "64", "86", "68", "98", "16", "D4", "A4", "5C", "CC", "5D", "65", "B6", "92"],
                ["6C", "70", "48", "50", "FD", "ED", "B9", "DA", "5E", "15", "46", "57", "A7", "8D", "9D", "84"],
                ["90", "D8", "AB", "00", "8C", "BC", "D3", "0A", "F7", "E4", "58", "05", "B8", "B3", "45", "06"],
                ["D0", "2C", "1E", "8F", "CA", "3F", "0F", "02", "C1", "AF", "BD", "03", "01", "13", "8A", "6B"],
                ["3A", "91", "11", "41", "4F", "67", "DC", "EA", "97", "F2", "CF", "CE", "F0", "B4", "E6", "73"],
                ["96", "AC", "74", "22", "E7", "AD", "35", "85", "E2", "F9", "37", "E8", "1C", "75", "DF", "6E"],
                ["47", "F1", "1A", "71", "1D", "29", "C5", "89", "6F", "B7", "62", "0E", "AA", "18", "BE", "1B"],
                ["FC", "56", "3E", "4B", "C6", "D2", "79", "20", "9A", "DB", "C0", "FE", "78", "CD", "5A", "F4"],
                ["1F", "DD", "A8", "33", "88", "07", "C7", "31", "B1", "12", "10", "59", "27", "80", "EC", "5F"],
                ["60", "51", "7F", "A9", "19", "B5", "4A", "0D", "2D", "E5", "7A", "9F", "93", "C9", "9C", "EF"],
                ["A0", "E0", "3B", "4D", "AE", "2A", "F5", "B0", "C8", "EB", "BB", "3C", "83", "53", "99", "61"],
                ["17", "2B", "04", "7E", "BA", "77", "D6", "26", "E1", "69", "14", "63", "55", "21", "0C", "7D"]]
    
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
Receives 16 bytes and shifts rows.
"""     
def InvShiftRows(hexStateArray):
    width, height = 4, 4
    newHexStateArray = [[0 for x in range(width)] for y in range(height)] 
    
    # row 1 doesn't change
    newHexStateArray[0][0] = hexStateArray[0][0]
    newHexStateArray[0][1] = hexStateArray[0][1]
    newHexStateArray[0][2] = hexStateArray[0][2]
    newHexStateArray[0][3] = hexStateArray[0][3]
    
    # shift 2nd row left by one
    newHexStateArray[1][0] = hexStateArray[1][3]
    newHexStateArray[1][1] = hexStateArray[1][0]
    newHexStateArray[1][2] = hexStateArray[1][1]
    newHexStateArray[1][3] = hexStateArray[1][2]
    
    
    # shift 3rd row left by two
    newHexStateArray[2][0] = hexStateArray[2][2]
    newHexStateArray[2][1] = hexStateArray[2][3]
    newHexStateArray[2][2] = hexStateArray[2][0]
    newHexStateArray[2][3] = hexStateArray[2][1]
    
    # shift 4th row left by 3
    newHexStateArray[3][0] = hexStateArray[3][1]
    newHexStateArray[3][1] = hexStateArray[3][2]
    newHexStateArray[3][2] = hexStateArray[3][3]
    newHexStateArray[3][3] = hexStateArray[3][0]            
    
    return newHexStateArray