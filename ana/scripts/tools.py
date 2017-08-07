"""
============================
script: tools.py
============================
date: 20170610 by Jianrong Deng
Purpose: various useful functions, including:
         flatten()

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
