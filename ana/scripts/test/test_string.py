# add 'commom' directory to python import search path
import sys
sys.path.append('../common/')
import const

print ('irb, idet, det_tag') 

for idet in range(1, int(const.N_det/2)+1): # 32 CCDs, index [1, 32]  = 2 * [1, 16]
    for irb in range (1, 3):  # 16 CCDs in blue, 16 in red
        if (irb == 1 ): 
           rb = 'r'
        else:  
           rb = 'b'
        if (idet <= 9  ):  # 00r-09r, 00b-09b
           det_tag = '0'+ str(int(idet)) + rb # for the index of 0-9, print out as 00-09
        else: 
           det_tag = str(int(idet)) + rb 
        print (irb, idet, det_tag)   
