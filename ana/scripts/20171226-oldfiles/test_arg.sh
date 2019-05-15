#!/bin/bash
#============================
# test_arg.sh
#============================
#   date: 20171208 by Jianrong Deng
#   purpose:
#   	bash script to check the input argument list of the command line bash script
#    usage: ./test_arg.sh {argument list}
#    example1: 
#           ./test_arg.sh 1 2 3 4 5  
#           Result:
#               [jdeng@localhost scripts]$ ./test_arg.sh 1 2 3 4 5 
#               $0 =  ./test_arg.sh
#               $1 =  1
#               $2 =  2
#               $# =  5
#               $@ =  1 2 3 4 5
#               NOTE: 
#               $0: returns bash command executed
#               $1, $i, $n: returns the ith argument
#               $#: returns the total number of input arguments to the bash script
#               $@: returns the list of input arguments to the bash script
#============================
echo "\$0 = " $0
echo "\$1 = " $1
echo "\$2 = " $2
echo "\$# = " $#
echo "\$@ = " $@

echo "NOTE: "
echo "\$0 print back the command line bash script"
echo "\$1, \$i, \$n: returns the ith argument"
echo "\$# returns the total number of input arguments to the bash script"
echo "\$@ returns the list of input arguments to the bash script"

