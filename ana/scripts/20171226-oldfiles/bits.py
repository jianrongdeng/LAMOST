"""
============================
script:  bits.py
============================
	date: 20170609 by Jianrong Deng
	purpose : modules on bit operations
	functions: 
		  bitCount()
                  testBit() setBit() clearBit() toggleBit()
"""
def bitCount(int_type):
    """
	Function: bitCount(int_type)
	    purpose: count number of bits set in int_type
	    Input   : int_type
	    Output  : number of bits set in int_type
    """
    count = 0
    while (int_type):
       # clear the least significant bit set
       # This works because each subtraction "borrows" from the lowest 1-bit.
       int_type &= int_type - 1 
       count +=1
    return (count)   

# Taken from 
#     https://wiki.python.org/moin/BitManipulation#CA-8a4270f706bae502366d3d0db78ac93aad6ac04a_2
####

# testBit() returns a nonzero result, 2**offset, if the bit at
# 'offset' is one.

def testBit(int_type, offset=0):
    mask = 1 << offset
    return(int_type & mask)

# setBit() returns an integer with the bit at 'offset' set to 1.

def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

# clearBit() returns an integer with the bit at 'offset' cleared.

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return(int_type & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0
# -> 1 and 1 -> 0.

def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)
    
