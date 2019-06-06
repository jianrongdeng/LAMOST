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
#============================
        '''
        purpose: initialize a "h_cluster" object

        '''

        from ROOT import TNtuple, TH1F, TH2F

        # Create some 1-D histograms, some 2-D histogram and an ntuple
        self.hx            = TH1F( 'hx', 'This is the x distribution', 4136, 0, 4136 )
        self.hy            = TH1F( 'hy', 'This is the y distribution', 4096, 0, 4096 )
        self.hpV           = TH1F( 'hpV', 'This is the pV distribution', 65536, 0, 65536)
        self.havgpV        = TH1F( 'havgpV', 'This is the average pV distribution', 300, 0, 3000 )
        self.hxy           = TH2F( 'hxy', 'y vs x', 100, 0, 4136, 100, 0, 4096)
        self.hxpV          = TH2F( 'hxpV', 'pV vs x', 100, 0, 4136, 1000, 0, 60000)
        self.hypV          = TH2F( 'hypV', 'pV vs y', 100, 0, 4096, 1000, 0, 60000)
        self.heigV0_eigV1  = TH2F( 'heigV0_eigV1', 'eigV0 vs eigV1; eigV0, eigV1', 100, 0, 2, 100, 0, 200)
        self.hweigV0_eigV1 = TH2F( 'hweigV0_eigV1', 'weigV0 vs weigV1; weigV0, weigV1', 100, 0, 2, 100, 0, 200)
        self.hcoef_eigV0   = TH2F( 'hcoef_eigV0', 'coef vs eigV0', 100, -1, 1, 100, 0, 2)
        self.hcoef_eigV1   = TH2F( 'hcoef_eigV1', 'coef vs eigV1', 100, -1, 1, 100, 0, 200)
        self.hwcoef_eigV0  = TH2F( 'hwcoef_eigV0', 'wcoef vs weigV0', 100, -1, 1, 100, 0, 2)
        self.hwcoef_eigV1  = TH2F( 'hwcoef_eigV1', 'wcoef vs weigV1', 100, -1, 1, 100, 0, 200)
        self.hcoef_wcoef   = TH2F( 'hcoef_wcoef', 'coef vs wcoef', 100, -1, 1, 100, -1, 1)
        self.ntuple = TNtuple( 'ntuple', 'cluster ntuple', 'mean:sstd:n_p:coef:eigVal_0:eigVal_1:w_coef:w_eigVal_0:w_eigVal_1:sumpV:avgpV' )

        # For speed, bind and cache the Fill member functions,
        self.histos = [ 'self.hx', 'self.hy', 'self.hpV', 'self.havgpV', 'self.hxy', 'self.hxpV', 'self.hypV', 'self.heigV0_eigV1', 'self.hweigV0_eigV1', 'self.hcoef_eigV0', 'self.hcoef_eigV1', 'self.hwcoef_eigV0', 'self.hwcoef_eigV1', 'self.hcoef_wcoef', 'self.ntuple' ]
        for name in self.histos:
           exec('%sFill = %s.Fill' % (name,name))

     

#============================

#============================
    def Fill(self, cluster): 
#============================
        '''
          Purpose: Fill histograms/ntuple.
          Input: 
             cluster: a cluster object
        '''
        # Fill histograms.
        # loop through all pixels in the cluster
        for ip in cluster: 
            self.hx.Fill(   ip[0])
            self.hy.Fill(   ip[1])
            self.hpV.Fill(  ip[2])
            self.hxy.Fill(  ip[0], ip[1])
            self.hxpV.Fill( ip[0], ip[2])
            self.hypV.Fill( ip[1], ip[2])
        # Fill in other 2-D histograms    
        self.havgpV.Fill(cluster.avgpV)
        self.heigV0_eigV1.Fill(cluster.eigVal[0], cluster.eigVal[1])
        self.hweigV0_eigV1.Fill(cluster.w_eigVal[0], cluster.w_eigVal[1])
        self.hcoef_eigV0.Fill(cluster.coef, cluster.eigVal[0])
        self.hcoef_eigV1.Fill(cluster.coef, cluster.eigVal[1])
        self.hwcoef_eigV0.Fill(cluster.w_coef, cluster.w_eigVal[0])
        self.hwcoef_eigV1.Fill(cluster.w_coef, cluster.w_eigVal[1])
        self.hcoef_wcoef.Fill(cluster.coef, cluster.w_coef)

        # Fill in the ntuple
        self.ntuple.Fill( 
            cluster.mean, 
            cluster.sstd, 
            cluster.n_p, 
            cluster.coef, 
            cluster.eigVal[0], 
            cluster.eigVal[1], 
            cluster.w_coef, 
            cluster.w_eigVal[0], 
            cluster.w_eigVal[1], 
            cluster.sumpV, 
            cluster.avgpV
        )




#============================


#============================
    def destroyCache(self): 

        # Destroy member functions cache.
        for name in self.histos:
           exec('del %sFill' % name)
        del self.histos
#============================
