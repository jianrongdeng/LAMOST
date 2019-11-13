'''
============================
test_pickle_data.py
============================

	date: 20190430 by Jianrong Deng
	purpose:
		test pickle_data module
	usage: python test_pickle_data.py	
        Working Directory: test_pickle_data_20190806/
        Input:  pickle_load.dat
        Output: pickle_dump.dat
                data.txt
============================
'''


import pickle_data as pd
# main # 

data_dir = 'test_cluster_pickle_data_20190809/'
#data_in =   'rb-01r-20160101174212-clusterClass.dat_image1_Cluster31_np242_sumpV_145871_pixels.dat'
data_in =   data_dir +  'pickle_load.dat'
data_out =  data_dir +  'pickle_dump.dat'
txt_out =   data_dir +  'data.txt'


# test pickle.load and pickle.dump
# pickle dump the list of pixels to a binary .dat file: 
# test pd.loadData
pixels =pd.loadData(data_in, debug = True, data_type='list', txt_fn=txt_out)
# test pd.printData
pd.printData(pixels, txt_fn=txt_out)
# test pd.dumpData
pd.dumpData(data_out, pixels,  debug = True, data_type='list', txt_fn=txt_out)
  

