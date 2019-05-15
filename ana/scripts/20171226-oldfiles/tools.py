"""
============================
script: tools.py
============================
date: 20170610 by Jianrong Deng
Purpose: various useful functions, including:
         flatten()
         getRatio()

"""

def flatten(items):
    """
    function used to flatten a list
    """
    non_list_items = []

    for item in items:
        if isinstance(item, list):
            for inner_item in flatten(item):
                yield inner_item
        else:
            non_list_items.append(item)

    yield non_list_items
#==========================

#==========================
def getRatio(num, denom, error= -1):
#==========================
    """
    purpose: get ratio of num/denom
    input: 
         num: numerator
         denom: denominator
         error: return value if denom == 0
    output:
         ratio = num/denom (if denom != 0)
               = error (if denom == 0 )
    """

    if denom == 0: 
         return error
    else:
         return num/denom

#==========================
