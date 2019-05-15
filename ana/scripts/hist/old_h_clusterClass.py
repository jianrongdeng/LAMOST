##============================
##h_clusterClass.py
##============================
##	date: 20190329 by Jianrong Deng
##	purpose:
##	    This program creates :
##		one dimensional histograms
##		two dimensional histograms
##		a memory-resident ntuple with the variables in the cluster Class
##
##	    These objects are filled with variables in the cluster Class and saved on a file
##      Source: modified from hsimple.py (see below)
##      Functions: 
##          FillClusterTree
##============================
##
#### \file
#### \ingroup tutorial_pyroot
## \notebook -js
##  This program creates :
##    - a one dimensional histogram
##    - a two dimensional histogram
##    - a profile histogram
##    - a memory-resident ntuple
##
##  These objects are filled with some random numbers and saved on a file.
##
## \macro_image
## \macro_code
##
## \author Wim Lavrijsen

## 

#==========================
## fuction 
def FillClusterTree(clusters, rootfile='cluster.root'):
    """
    purpose: 
        read in clusters data (in cluster Class format)
        Fill a cluster Ntuple and save to the rootfile
    input : 
       clusters: clusters data in the cluster Class format
       rootfile: the filename for the root output file
    output: 
    """

    #from ROOT import TFile, TNtuple, TTree
    from ROOT import TFile
    from ROOT import gROOT, gStyle
    from ROOT import TNtuple, TH1F, TH2F
    #from ROOT import AddressOf
    #import cluster

    # root style
    gStyle.SetOptStat(11111111) 
    gStyle.SetLineColor(2) 
    gStyle.SetLineWidth(4) 
    gStyle.SetMarkerColor(3) 
    gStyle.SetMarkerStyle(21) 
    gROOT.ForceStyle() 

    # Create a new ROOT binary machine independent file.
    # Note that this file may contain any kind of ROOT objects, histograms,
    # pictures, graphics objects, detector geometries, tracks, events, etc..
    # This file is now becoming the current directory.

    hfile = gROOT.FindObject(rootfile)
    if hfile:
       hfile.Close()
    hfile = TFile( rootfile, 'RECREATE', 'ROOT file for the cluster class' )

    # Create some histograms, a profile histogram and an ntuple
    hx    = TH1F( 'hx', 'This is the x distribution', 4136, 0, 4136 )
    hy    = TH1F( 'hy', 'This is the y distribution', 4096, 0, 4096 )
    hpV   = TH1F( 'hpV', 'This is the pV distribution', 65536, 0, 65536)
    hxy  = TH2F( 'hxy', 'y vs x', 100, 0, 4136, 100, 0, 4096)
    hxpV  = TH2F( 'hxpV', 'pV vs x', 100, 0, 4136, 1000, 0, 60000)
    hypV  = TH2F( 'hypV', 'pV vs y', 100, 0, 4096, 1000, 0, 60000)
    heigV0_eigV1  = TH2F( 'heigV0_eigV1', 'eigV0 vs eigV1; eigV0, eigV1', 100, 0, 2, 100, 0, 200)
    hweigV0_eigV1  = TH2F( 'hweigV0_eigV1', 'weigV0 vs weigV1; weigV0, weigV1', 100, 0, 2, 100, 0, 200)
    hcoef_eigV0  = TH2F( 'hcoef_eigV0', 'coef vs eigV0', 100, -1, 1, 100, 0, 2)
    hcoef_eigV1  = TH2F( 'hcoef_eigV1', 'coef vs eigV1', 100, -1, 1, 100, 0, 200)
    hwcoef_eigV0  = TH2F( 'hwcoef_eigV0', 'wcoef vs weigV0', 100, -1, 1, 100, 0, 2)
    hwcoef_eigV1  = TH2F( 'hwcoef_eigV1', 'wcoef vs weigV1', 100, -1, 1, 100, 0, 200)
    hcoef_wcoef  = TH2F( 'hcoef_wcoef', 'coef vs wcoef', 100, -1, 1, 100, -1, 1)
    ntuple = TNtuple( 'ntuple', 'cluster ntuple', 'mean:sstd:n_p:coef:eigVal_0:eigVal_1:w_coef:w_eigVal_0:w_eigVal_1:sumpV:avgpV' )


    # For speed, bind and cache the Fill member functions,
    histos = [ 'hx', 'hy', 'hpV', 'hxy', 'hxpV', 'hypV', 'heigV0_eigV1', 'hweigV0_eigV1', 'hcoef_eigV0', 'hcoef_eigV1', 'hwcoef_eigV0', 'hwcoef_eigV1', 'hcoef_wcoef', 'ntuple' ]
    for name in histos:
       exec('%sFill = %s.Fill' % (name,name))

    # five images
    # for im in range(len(clusters)):

    '''
    # Note that the file is automatically closed when application terminates
    # or when the file destructor is called.
    ## \file
    ## \ingroup tutorial_pyroot
    ## \notebook -js
    ##  This program creates :
    ##    - a one dimensional histogram
    ##    - a two dimensional histogram
    ##    - a profile histogram
    ##    - a memory-resident ntuple
    ##
    ##  These objects are filled with some random numbers and saved on a file.
    ##
    ## \macro_image
    ## \macro_code
    ##
    ## \author Wim Lavrijsen

    from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
    from ROOT import gROOT, gBenchmark, gRandom, gSystem, Double

    # Create a new canvas, and customize it.
    c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
    c1.SetFillColor( 42 )
    c1.GetFrame().SetFillColor( 21 )
    c1.GetFrame().SetBorderSize( 6 )
    c1.GetFrame().SetBorderMode( -1 )

    # Create a new ROOT binary machine independent file.
    # Note that this file may contain any kind of ROOT objects, histograms,
    # pictures, graphics objects, detector geometries, tracks, events, etc..
    # This file is now becoming the current directory.

    hfile = gROOT.FindObject( 'py-hsimple.root' )
    if hfile:
       hfile.Close()
    hfile = TFile( 'py-hsimple.root', 'RECREATE', 'Demo ROOT file with histograms' )

    # Create some histograms, a profile histogram and an ntuple
    hpx    = TH1F( 'hpx', 'This is the px distribution', 100, -4, 4 )
    hpxpy  = TH2F( 'hpxpy', 'py vs px', 40, -4, 4, 40, -4, 4 )
    hprof  = TProfile( 'hprof', 'Profile of pz versus px', 100, -4, 4, 0, 20 )
    ntuple = TNtuple( 'ntuple', 'Demo ntuple', 'px:py:pz:random:i' )

    # Set canvas/frame attributes.
    hpx.SetFillColor( 48 )

    gBenchmark.Start( 'hsimple' )

    # Initialize random number generator.
    gRandom.SetSeed()
    rannor, rndm = gRandom.Rannor, gRandom.Rndm

    # For speed, bind and cache the Fill member functions,
    histos = [ 'hpx', 'hpxpy', 'hprof', 'ntuple' ]
    for name in histos:
       exec('%sFill = %s.Fill' % (name,name))

    # Fill histograms randomly.
    px, py = Double(), Double()
    kUPDATE = 1000
    for i in range( 25000 ):
     # Generate random values.
       rannor( px, py )
       pz = px*px + py*py
       random = rndm(1)

     # Fill histograms.
       hpx.Fill( px )
       hpxpy.Fill( px, py )
       hprof.Fill( px, pz )
       ntuple.Fill( px, py, pz, random, i )

     # Update display every kUPDATE events.
       if i and i%kUPDATE == 0:
          if i == kUPDATE:
             hpx.Draw()

          c1.Modified()
          c1.Update()

          if gSystem.ProcessEvents():            # allow user interrupt
             break

    # Destroy member functions cache.
    for name in histos:
       exec('del %sFill' % name)
    del histos

    gBenchmark.Show( 'hsimple' )

    # Save all objects in this file.
    hpx.SetFillColor( 0 )
    hfile.Write()
    hpx.SetFillColor( 48 )
    c1.Modified()
    c1.Update()

    # Note that the file is automatically closed when application terminates
    # or when the file destructor is called.
    '''
