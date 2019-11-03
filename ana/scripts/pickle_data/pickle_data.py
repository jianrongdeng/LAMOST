"""
============================
pickle_pixels.py
============================

	date: 20190806 by Jianrong Deng
	purpose:
		Pickle  data (default is a list of candidate pixels) to a binary .dat file 
                Use pickle.dump and pickle.load for write/read data to/from a file. 
============================
"""

import pickle

import sys

#============================
def printData(data, txt_fn=sys.stdout, data_type = 'list'):
#============================
    """
    purpose: print data (default data format is a list)
    input : 
        data
             default: a list
        txt_fn = sys.stdout: 
             default: print to sys.stdout
             if a txt_fn filename is given, print to the txt_fn file     
        data_type: default is 'list'

    """
    if (txt_fn == sys.stdout) : print(data)

    # open output file with "w"
    else:
        try:
            with open(txt_fn, 'w' ) as txt_file:
                if (data_type == 'list'): 
                    N = len(data)
                    for ip in range(N):
                         print ( data[ip], file=txt_file)
                    print('number of items in the ', data_type, ' =  ', N,  file=txt_file)
                    print('filename = ', txt_fn,  file=txt_file)
        except IOError as err:
           print('File error: ',   str(err))
        finally:
           txt_file.close()
    return           

#============================


#============================
def dumpData(file_out, data , debug = False, data_type='list', txt_fn=sys.stdout):
#============================
    """
    purpose: dump data (default is a list,  or other data format) to an output binary data file
    input :  filename and  data (default is a list)
    optional inputs:
            debug: debug flag
            data_type: the data_type of the input data
            txt_fn: the output filename of the print out text (if debug == True)
    """
    # save list to an output file
    try:
        with open(file_out, "wb") as data_file:
            pickle.dump(data, data_file)
    except IOError as err:
        print('File error: ',   str(err))
    except pickle.PickleError as perr:
        print('picklingerror:',  str(perr))

    if debug: printData(data, data_type = data_type, txt_fn=txt_fn)

    return            
#============================


#============================
def loadData(file_in, debug = False, data_type='list', txt_fn=sys.stdout):
#============================
    """
    purpose: load data (default is a list) from an input data file
    input :  file_in
    output : data

    """
    # load a list from the input file
    try:
        with open(file_in, "rb") as data_file:
            data = pickle.load(data_file)
    except IOError as err:
        print('file error: ',   str(err))
    except pickle.PickleError as perr:
        print('picklingerror:',  str(perr))

    if debug: printData(data, data_type = data_type, txt_fn=txt_fn)
    
    return data
#============================


