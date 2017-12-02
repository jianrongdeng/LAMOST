

"""
purpose: test the pass of parameter to function and if the change to
parameters remains locally or globally after the call.
"""

#==========================
# note: when passing an int to a function, any change to the int will remains LOCALLY
def call_int (in_int):
   print("in_int = ", in_int)
   in_int = in_int + 1
   return 
#==========================

#==========================
# note: when passing a string to a function, any change to the string will remains LOCALLY
def call_str (in_str):
   print("in_str = ", in_str)
   in_str = in_str + 'b' 
   return 
#==========================

#==========================
# note: when passing a list to a function, any change to the string will  be GLOBAL
def call_list (in_list):
   print("in_list = ", in_list)
   in_list.append('b')
   in_list[2] = 'e'
   return 
#==========================

in_int = 9
call_int(in_int)
print("in_int = ", in_int)

in_str = 'abc'
call_str(in_str)
print("in_str = ", in_str)

in_list = ['a', 'b', 'c']
call_list(in_list)
print("in_list = ", in_list)

