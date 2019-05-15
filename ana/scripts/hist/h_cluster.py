"""
============================
h_cluster.py
============================
	date: 20190515 by Jianrong Deng

	purpose:
		h_cluster class

  	    This class creates :
  		one dimensional histograms
  		two dimensional histograms
  		a memory-resident ntuple with the variables in the cluster Class 

============================
"""

#============================
class h_cluster():
#============================
#============================
    def __init__(self): 
        '''
        purpose: initialize a "h_cluster" object

        '''

        from ROOT import TNtuple, TH1F, TH2F

        # Create some 1-D histograms, some 2-D histogram and an ntuple
        hx            = TH1F( 'hx', 'This is the x distribution', 4136, 0, 4136 )
        hy            = TH1F( 'hy', 'This is the y distribution', 4096, 0, 4096 )
        hpV           = TH1F( 'hpV', 'This is the pV distribution', 65536, 0, 65536)
        hxy           = TH2F( 'hxy', 'y vs x', 100, 0, 4136, 100, 0, 4096)
        hxpV          = TH2F( 'hxpV', 'pV vs x', 100, 0, 4136, 1000, 0, 60000)
        hypV          = TH2F( 'hypV', 'pV vs y', 100, 0, 4096, 1000, 0, 60000)
        heigV0_eigV1  = TH2F( 'heigV0_eigV1', 'eigV0 vs eigV1; eigV0, eigV1', 100, 0, 2, 100, 0, 200)
        hweigV0_eigV1 = TH2F( 'hweigV0_eigV1', 'weigV0 vs weigV1; weigV0, weigV1', 100, 0, 2, 100, 0, 200)
        hcoef_eigV0   = TH2F( 'hcoef_eigV0', 'coef vs eigV0', 100, -1, 1, 100, 0, 2)
        hcoef_eigV1   = TH2F( 'hcoef_eigV1', 'coef vs eigV1', 100, -1, 1, 100, 0, 200)
        hwcoef_eigV0  = TH2F( 'hwcoef_eigV0', 'wcoef vs weigV0', 100, -1, 1, 100, 0, 2)
        hwcoef_eigV1  = TH2F( 'hwcoef_eigV1', 'wcoef vs weigV1', 100, -1, 1, 100, 0, 200)
        hcoef_wcoef   = TH2F( 'hcoef_wcoef', 'coef vs wcoef', 100, -1, 1, 100, -1, 1)
        ntuple = TNtuple( 'ntuple', 'cluster ntuple', 'mean:sstd:n_p:coef:eigVal_0:eigVal_1:w_coef:w_eigVal_0:w_eigVal_1:sumpV:avgpV' )

        # For speed, bind and cache the Fill member functions,
        histos = [ 'hx', 'hy', 'hpV', 'hxy', 'hxpV', 'hypV', 'heigV0_eigV1', 'hweigV0_eigV1', 'hcoef_eigV0', 'hcoef_eigV1', 'hwcoef_eigV0', 'hwcoef_eigV1', 'hcoef_wcoef', 'ntuple' ]
        for name in histos:
           exec('%sFill = %s.Fill' % (name,name))

     

#============================

