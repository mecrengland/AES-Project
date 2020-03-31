# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 12:59:58 2020

@author: hogan
"""

def polyDivRem(numer, denom):
    
    # Degree of denominator (not actual degree but 'highest degree spot')
    denomDeg = -1
    # Finds highest degree of denominator
    for i in range(len(denom)):
        if(not denom[i] == 0):
            denomDeg = i
            break
    if(denomDeg == -1):
        return "Null Denominator"
    denom = denom[denomDeg:]
    
    # Move through numerator and divide
    for i in range(len(numer)):
        if((not numer[i] == 0) and (len(denom) <= len(numer)-i)):
            # Result used to subtract in long division
            divResult = numer[i]/denom[0]
            
            # Creates array to subtract from numerator
            subArr = []
            for j in range (len(denom)):
                subArr.append(divResult * denom[j])
            
            # Subtracts values from numerator
            for j in range (len(subArr)):
                numer[i+j] = numer[i+j] - subArr[j]
        else:
            if(numer[i] == 0):
                continue
            else:
                return numer
        
    return numer