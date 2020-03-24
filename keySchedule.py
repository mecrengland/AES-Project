# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 12:37:47 2020

@author: hogan
"""

import math

# Global Variables:
Nr = 10

sBox =      [["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
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

RC = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54]
keyExpansion = []

def keySchedule128(keyArr):
    
    key = ""
    
    # Convert to binary
    for i in range(len(keyArr)):
        keyArr[i] = bin(int(keyArr[i], 16))[2:]
        while(len(keyArr[i]) < 8):
            keyArr[i] = "0" + keyArr[i]
        key += keyArr[i]
    
    # Initial 4 byte input
    for i in range(0,4):
        keyExpansion.append(key[i*32:(i+1)*32])
    
    # Nr rounds of key functions
    for keyRound in range(0,Nr):
        for i in range(0,4):
            # XOR 0 w/ g(3), 1 w/ 0, 2 w/ 1, 3 w/ 2
            if(i == 0):
                keyExpansion.append(XOR(keyExpansion[keyRound*4], funcG(keyExpansion[keyRound*4+3], keyRound)))
            else:
                if(keyRound == 0):
                    keyExpansion.append(XOR(keyExpansion[i], keyExpansion[i+3]))
                else:
                    keyExpansion.append(XOR(keyExpansion[keyRound*4+i], keyExpansion[keyRound*4+i+3]))
                
    return keyExpansion
        

def funcG(keyBytes, rnd):
    
    # Shift MS 8 bits to LS 8 bits
    keyBytes = keyBytes[8:32] + keyBytes[0:8]
    returnBytes = ""
    
    # For each byte, exchange exchange w/ S-box
    for i in range(0,4):
        preS1 = int(keyBytes[i*8:(i+1)*8-4], 2)
        preS2 = int(keyBytes[i*8+4:(i+1)*8], 2)
        postS = bin(int(sBox[preS1][preS2], 16))[2:]
        while (len(postS) < 8):
            postS = "0" + postS
        returnBytes += postS
    
    # Exclusive OR with round coefficients on first 8 bits
    returnBytes = XOR(returnBytes[:8], bin(RC[rnd])[2:]) + returnBytes[8:]
    
    return returnBytes


def XOR(str1, str2):
    
    # If strings aren't same length pad with 0's
    if (len(str1) < len(str2)):
        while(len(str1) < len(str2)):
            str1 = "0" + str1
    elif (len(str1) > len(str2)):
        while(len(str1) > len(str2)):
            str2 = "0" + str2
    
    # For each bit, if same -> 0, if not same -> 1
    for bit in range(0, len(str1)):
        if(str1[bit] != str2[bit]):
            str1 = str1[:bit] + "1" + str1[bit+1:]
        else:
            str1 = str1[:bit] + "0" + str1[bit+1:]
            
    return str1







