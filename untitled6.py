# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 19:39:16 2020

@author: Megan
"""

def hexToBinary(value):      
    value = str(bin(ord(value))[2:])
    while(len(value) < 8):
            value = "0" + value
    
    print(value)
    
    decimalValue = int(value, 2)
    value = str(hex(decimalValue)[2:])
    
    print(value)
    scale = 16
    value = str((bin(int(value, scale)).zfill(8))[2:] )
    while(len(value) < 8):
            value = "0" + value        
    
    print value  