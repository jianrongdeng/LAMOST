'''
============================
cluster_display.py
============================

	date: 20190429 by Jianrong Deng
	purpose:
		display cluster events
        input: 
               1. a cluster data file (in cluster Class format)
               2. a cluster list file (in pixle list format)
               3. FIVE original image files (in fit format)
               note: one cluster data file corresponds to FIVE image files
        output:
               1. a scatter plot of a selected cluster
               2. a sub-plot (of the from the original image fit file)
               3. an event header in txt
        
        command line optional input:
               1. cut_n_P: a cut on the number of pixel for one cluster
               2. print out flag: if True, save output plots to ps file
============================
'''

#==========================
def list2graph(cl, flag_save = True, graph_filename='graph.eps', txt_filename='cluster.txt'):
    """
    purpose: 
    input : 
          1. cl: a cluster data in cluster Class format
          2. flags:
             a. flag_save: if True, save the scatter plot to eps file
          3. graph_filename: if (flag_save): save graph to file graph_filename   
          4. txt_filename: if (flag_save): save cluster info to file txt_filename   
    output: 
          1. a graph of the input pixel list

    """
#==========================

    from ROOT import TGraph
    from ROOT import TCanvas
    #from ROOT import gSystem
    from ROOT import gStyle
    from ROOT import gROOT


    # print cluster information
    cl.printCluster(txt_filename)

 

    # root style
    gStyle.SetOptStat(11111111) 
    gStyle.SetLineColor(2) 
    gStyle.SetLineWidth(4) 
    # color: black = 1; red = 2; green = 3; blue = 4
    gStyle.SetMarkerColor(2) 
    gStyle.SetMarkerStyle(21) 
    gStyle.SetMarkerSize(2) 
    gROOT.ForceStyle() 


    # Create a new canvas, and customize it.
    c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
    c1.SetGrid() 
    c1.SetFillColor( 42 )
    c1.GetFrame().SetFillColor( 21 )
    c1.GetFrame().SetBorderSize( 6 )
    c1.GetFrame().SetBorderMode( -1 )

    gr = TGraph(cl.n_p, cl.xs, cl.ys )
    gr.SetTitle('Cluster Candidate; pixels; pixels') 
    gr.SetFillColor( 48 )
    gr.Draw("A*") # "A": draw axis, "*": draw a "*" on data points

    c1.Modified()
    c1.Update()
    #c1.Draw()
    #c1.Show()
    #gSystem.Sleep ( 1000)

    '''
    if gSystem.ProcessEvents():            # allow user interrupt
         break
         '''
    if (flag_save ): c1.Print(graph_filename)

    # Destroy member functions cache.
    del gr, cl


#==========================

#==========================
def list2TH2F(cl, flag_save = True, hist_filename='hist2F.eps', txt_filename='cluster.txt'):
    """
    purpose: 
    input : 
          1. cl: a cluster data in cluster Class format
          2. flags:
             a. flag_save: if True, save the scatter plot to eps file
          3. hist_filename: if (flag_save): save the TH2F hist to file hist_filename   
          4. txt_filename: if (flag_save): save cluster info to file txt_filename   
    output: 
          1. a TH2F histogram of the input pixel list

    """
#==========================

    from ROOT import TH2F
    from ROOT import TCanvas
    #from ROOT import gSystem
    from ROOT import gStyle
    from ROOT import gROOT
    import numpy as np


    # print cluster information
    cl.printCluster(txt_filename)

 

    # root style
    gStyle.SetOptStat(11111111) 
    gStyle.SetLineColor(2) 
    gStyle.SetLineWidth(4) 
    # color: black = 1; red = 2; green = 3; blue = 4
    gStyle.SetMarkerColor(2) 
    gStyle.SetMarkerStyle(21) 
    gStyle.SetMarkerSize(2) 
    gROOT.ForceStyle() 


    # Create a new canvas, and customize it.
    c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200, 10, 700, 500 )
    c1.SetGrid() 
    c1.SetFillColor( 42 )
    c1.GetFrame().SetFillColor( 21 )
    c1.GetFrame().SetBorderSize( 6 )
    c1.GetFrame().SetBorderMode( -1 )

    hxy = TH2F('hxy', 'y vs x', int(cl.deltax), int(cl.xmin), int(cl.xmax), int(cl.deltay), int(cl.ymin), int(cl.ymax) )
    i_xs = [ (int)(xi) for xi in cl.xs] 
    print ('i_xs', i_xs)
    i_ys = [ (int)(yi) for yi in cl.ys] 
    print ('i_ys', i_ys)
    #hxy.FillN(len(cl.xs), np.ndarray(i_xs), np.ndarray(i_ys). np.ndarray(cl.pVs))
    #i_xs = [250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262]
    #i_ys = [1510, 1510, 1510, 1510, 1510, 1510, 1510, 1510, 1510, 1510, 1510, 1510, 1510]
    # ??? TypeError:
    # " void TH2::FillN(int ntimes, const double* x, const double* y, const double* w, int stride = 1) =>
    # could not convert argument 2
    hxy.FillN(len(cl.xs), i_xs, i_ys, cl.pVs)
    #hxy.FillN(len(cl.xs), i_xs, i_ys, 1)
    hxy.SetTitle('Cluster Candidate; pixels; pixels') 
    hxy.SetFillColor( 48 )
    #hxy.Draw("A*") # "A": draw axis, "*": draw a "*" on data points
    hxy.Draw("colz") # "A": draw axis, "*": draw a "*" on data points

    c1.Modified()
    c1.Update()
    #c1.Draw()
    #c1.Show()
    #gSystem.Sleep ( 1000)

    '''
    if gSystem.ProcessEvents():            # allow user interrupt
         break
         '''
    if (flag_save ): c1.Print(hist_filename)

    # Destroy member functions cache.
    del h2F, cl

#==========================


#==========================
# main function
#==========================



