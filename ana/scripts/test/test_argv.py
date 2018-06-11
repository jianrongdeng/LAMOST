"""
============================
test_argv.py
============================
	date: 20180116 by Jianrong Deng
        Purpose: test the use of sys.argv
           sys.argv: command line arguments
           sys.argv[0] is the input script name
============================
"""

import sys

# sys.argv[0] is the script name
print( sys.argv[0])
# argv[1:] are command line arguments
if len(sys.argv) > 1 :
   print( sys.argv[1:])
