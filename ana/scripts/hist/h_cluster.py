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
        self.heigV0        = TH1F( 'heigV0', 'This is the eigenvalue 0 distribution', 1000, 0, 5)
        self.heigV1        = TH1F( 'heigV1', 'This is the eigenvalue 1 distribution', 1000, 0, 1000)
        self.hweigV0       = TH1F( 'hweigV0', 'This is the weighted eigenvalue 0 distribution', 1000, 0, 5)
        self.hweigV1       = TH1F( 'hweigV1', 'This is the weighted eigenvalue 1 distribution', 1000, 0, 1000)
        self.hratio_eigVal      = TH1F( 'hratio_eigVal      ', 'This is the distribution of eigVal[0]/eigVal[1]', 1000, 0, 1)
        self.hratio_w_eigVal    = TH1F( 'hratio_w_eigVal    ', 'This is the distribution of w_eigVal[0]/w_eigVal[1]', 1000, 0, 1) 
        self.hratio_pVmax_sumpV = TH1F( 'hratio_pVmax_sumpV ', 'This is the distribution of pVmax/sumpV', 1000, 0, 1)
        self.hratio_pVmax_avgpV = TH1F( 'hratio_pVmax_avgpV ', 'This is the distribution of pVmax/argpV', 1000, 0, 1)
        self.hxy           = TH2F( 'hxy', 'y vs x; x; y', 100, 0, 4136, 100, 0, 4096)
        self.hxpV          = TH2F( 'hxpV', 'pV vs x; x; pV', 100, 0, 4136, 1000, 0, 60000)
        self.hypV          = TH2F( 'hypV', 'pV vs y; y; pV', 100, 0, 4096, 1000, 0, 60000)
        self.heigV0_eigV1  = TH2F( 'heigV0_eigV1', 'eigV1 vs eigV0; eigV0; eigV1', 100, 0, 2, 100, 0, 200)
        self.hweigV0_eigV1 = TH2F( 'hweigV0_eigV1', 'weigV1 vs weigV0; weigV0; weigV1', 100, 0, 2, 100, 0, 200)
        self.hcoef_eigV0   = TH2F( 'hcoef_eigV0', 'eigV0 vs coef; coef; eigV0', 100, -1, 1, 100, 0, 2)
        self.hcoef_eigV1   = TH2F( 'hcoef_eigV1', 'eigV1 vs coef; coef; eigV1', 100, -1, 1, 100, 0, 200)
        self.hwcoef_eigV0  = TH2F( 'hwcoef_eigV0', 'weigV0 vs wcoef; wcoef; weigV0', 100, -1, 1, 100, 0, 2)
        self.hwcoef_eigV1  = TH2F( 'hwcoef_eigV1', 'weigV1 vs wcoef; wcoef; weigV1', 100, -1, 1, 100, 0, 200)
        self.hcoef_wcoef   = TH2F( 'hcoef_wcoef', 'wcoef vs coef; coef; wcoef', 100, -1, 1, 100, -1, 1)
        self.hnp_coef   = TH2F( 'hnp_coef', 'coef vs number of pixels; number of pixels; coef', 1000, 0, 1000, 100, -1, 1)
        self.hnp_wcoef   = TH2F( 'hnp_wcoef', 'wcoef vs number of pixels; number of pixels; wcoef', 1000, 0, 1000, 100, -1, 1)

        self.ntuple = TNtuple( 'ntuple', 'cluster ntuple', 'mean:sstd:n_p:coef:eigVal_0:eigVal_1:w_coef:w_eigVal_0:w_eigVal_1:sumpV:avgpV:ratio_eigVal:ratio_w_eigVal:ratio_pVmax_sumpV:ratio_pVmax_avgpV' )

        # For speed, bind and cache the Fill member functions,
        self.histos = [ 'self.hx', 'self.hy', 'self.hpV', 'self.havgpV', 'self.heigV0', 'self.heigV1', 'self.hweigV0', 'self.hweigV1', 'self.hratio_eigVal', 'self.hratio_w_eigVal', 'self.hratio_pVmax_sumpV', 'self.hratio_pVmax_avgpV', 'self.hxy', 'self.hxpV', 'self.hypV', 'self.heigV0_eigV1', 'self.hweigV0_eigV1', 'self.hcoef_eigV0', 'self.hcoef_eigV1', 'self.hwcoef_eigV0', 'self.hwcoef_eigV1', 'self.hcoef_wcoef', 'self.hnp_coef', 'self.hnp_wcoef', 'self.ntuple' ]

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
        # Fill in other 1-D histograms    
        self.havgpV.Fill(cluster.avgpV)
        self.heigV0.Fill(cluster.eigVal[0])
        self.heigV1.Fill(cluster.eigVal[1])
        self.hweigV0.Fill(cluster.w_eigVal[0])
        self.hweigV1.Fill(cluster.w_eigVal[1])
        # Fill in 1D ratios
        self.hratio_eigVal.Fill(     cluster.ratio_eigVal     )
        self.hratio_w_eigVal.Fill(   cluster.ratio_w_eigVal   )
        self.hratio_pVmax_sumpV.Fill(cluster.ratio_pVmax_sumpV)
        self.hratio_pVmax_avgpV.Fill(cluster.ratio_pVmax_avgpV)
        # Fill in other 2-D histograms    
        self.heigV0_eigV1.Fill(cluster.eigVal[0], cluster.eigVal[1])
        self.hweigV0_eigV1.Fill(cluster.w_eigVal[0], cluster.w_eigVal[1])
        self.hcoef_eigV0.Fill(cluster.coef, cluster.eigVal[0])
        self.hcoef_eigV1.Fill(cluster.coef, cluster.eigVal[1])
        self.hwcoef_eigV0.Fill(cluster.w_coef, cluster.w_eigVal[0])
        self.hwcoef_eigV1.Fill(cluster.w_coef, cluster.w_eigVal[1])
        self.hcoef_wcoef.Fill(cluster.coef, cluster.w_coef)
        self.hnp_coef.Fill(cluster.n_p, cluster.coef)
        self.hnp_wcoef.Fill(cluster.n_p, cluster.w_coef)

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
            cluster.avgpV,
            cluster.ratio_eigVal,
            cluster.ratio_w_eigVal,
            cluster.ratio_pVmax_sumpV,
            cluster.ratio_pVmax_avgpV
        )




#============================


#============================
    def destroyCache(self): 

        # Destroy member functions cache.
        for name in self.histos:
           exec('del %sFill' % name)
        del self.histos
#============================
