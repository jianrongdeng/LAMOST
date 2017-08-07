"""
=======================================
script: subtract_overscan_median.py
=======================================
        purpose:
                 take 5 biased data images, subtract overscan (OS) of
                 each image, then generate the median image from the 5
                 OS subtracted image.
        Output:
                 five image, each with: out image = in - OS - median

*By: Jianrong Deng 20170523


STEPs : take one biased data image_i, calculate mean and standard deviation (std) of the image
	 1. First calculate the mean and std of overscan(OS) regions:
	     for each image, mean  =  [ 
					    average over pixels (y=[0, 4136], x=[4096,4128]), 
					    average over pixels (y=[0, 4136], x=[4128,4160])
					    ]
	     ( due to two readout channels for each CCD camera. )				
	     for each image, std  =  [ 
	 				sample over pixels (y=[0, 4136], x=[4096, 4128]),
	 				sample over pixels (y=[0, 4136], x=[4128, 4160])
					]
	 2. Then calculate the net = data - OS
	     for each image, net  mean  =  (data - OS )[ 
					    average over pixels (y=[0, 4136], x=[   0, 2048]),
					    average over pixels (y=[0, 4136], x=[2048, 4096])
					    ]
	     ( due to two readout channels for each CCD camera. )				
	     for each image, std  =  [ 
	 				sample over pixels (y=[0, 4136], x=[   0, 2048]),
	 				sample over pixels (y=[0, 4136], x=[2048, 4096])
					]
	     ( due to two readout channels for each CCD camera. )				
	  3. generate the median biased image: median = median(net) 

Input: 5 biased data
Output: OS_mean, OS_std
        net = (data-OS_mean) 
        real = (data-OS_mean) - median 
-------------------
"""


from astropy.io import fits
import numpy as np
import statistics as sts
import matplotlib.pyplot as plt
#import matplotlib.markers as mks

DEBUG = 'True'

##############################################################################
# read in 5 biased files
dir_in = '/Users/jdeng/baiduCloudDisk/LAMOST/data/20150923/bias/'
dir_out = '/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/20150923/bias/'
det = 'rb-16r-'
time = [
'20150923234527-10000-82496145',
'20150923234936-10000-82496149',
'20150923235345-10000-82496153',
'20150923235754-10000-82496157',
'20150924000612-10000-82496166'
]
postfix_in = '.fit.gz'
postfix_out = '.fit'

# define overscan region
N_t = len(time) # number of biased images
N_y = 4136 # total number of pixels in y direction
N_x = 4096 # the last pixel (in x) before overscan bands
N_os = 2  # number of overscan regions
nbins = 32  # number of total x bins in overscan regions
os_x_min = []
os_x_max = []
data_x_min = [] # define two amplifier regions in data
data_x_max = []
# [4096, 4096 + 32], [4096 + 32, 4096 + 32 + 32]
# note: in python, an array with index [a, b], a will be inclusive, b will be exclusive
for i in range(2):
   os_x_min.append(N_x  + i * nbins )
   os_x_max.append( os_x_min[i] + nbins )
# region 1: x = [0 : N_x/N_os]
# region 2: x = [N_x/N_os : N_x]
   data_x_min.append(int(i * N_x/N_os) )
   data_x_max.append(int(data_x_min[i] + N_x/N_os) )
   if DEBUG:
      print (data_x_min[i], data_x_max[i])

cn_y =  np.zeros((N_y))
cn_x =  np.zeros((N_os * nbins))
os_mean = np.zeros((N_y,N_os))
os_sstd = np.zeros((N_y,N_os)) 
os_pstd = np.zeros((N_y,N_os)) 
overscan= np.zeros((N_y,N_x))
net     = np.zeros((N_y,N_x, N_t))
real    = np.zeros((N_y,N_x, N_t))

file_median       = dir_out + det + time[0] + '-median-over5images' + postfix_out    # output image used for the overscan subtraction
his_real_out = []
file_real = []

for k in range(N_t):
    t_i = time[k]
    # input and output file names
    file_os       = dir_out + det + t_i + '-overscan' + postfix_out    # output image used for the overscan subtraction
    file_net      = dir_out + det + t_i + '-sub_overscan' + postfix_out    # output image = input - overscan 
    file_real.append( dir_out + det + t_i + '-sub_overscan-sub_bias' + postfix_out)    # output image = input - overscan 
    file_in       = dir_in  + det + t_i + postfix_in             # input biased data files
    fig_out       = dir_out + 'figures/' + det + t_i + '-overscan-mean-sstd-x-y.png'   # output overscan and sstd distribution over x and over y
    his_out       = dir_out + 'figures/' + det + t_i + '-hist-sub_overscan.png'   # output histograms of (data - OS)
    his_real_out.append( dir_out + 'figures/' + det + t_i + '-hist-sub_overscan-sub_bias.png')   # output histograms of (data - OS - bias-median)

    images = fits.getdata(file_in, ext=0)

    for i in range(N_os):
	    for j_y in range(N_y):
		    # the sub-array of the overscan region
		    os_data =  (images[j_y, os_x_min[i]:os_x_max[i] ] )  # note: the first index is y-axis, the second axis is x
		    cn_y[j_y] = j_y # used in plotting 
# calculate mean and std deviation using values in the overscan region
		    os_mean[j_y, i] =  np.mean(os_data)   #  calculate the mean for the two overscan regions
		    # sample standard deviation
		    os_sstd[j_y, i] =  (sts.stdev(os_data.flatten()))
		    # population standard deviation
		    os_pstd[j_y, i] = (np.std(os_data))
		    # subtract overscan
		    overscan[j_y, data_x_min[i]:data_x_max[i]] =  os_mean[j_y, i]
		    net[j_y, data_x_min[i]:data_x_max[i],k] = images[j_y, data_x_min[i]:data_x_max[i] ] - os_mean[j_y, i]



		    if DEBUG :
		       if j_y < 5:
                          print (k,i, j_y, os_x_min[i], os_x_max[i], os_mean[j_y, i],'\t',  os_sstd[j_y, i], '\t',  os_pstd[j_y, i])
                          print (images[j_y, data_x_min[i]:data_x_min[i] + 5 ])
                          print (net[j_y, data_x_min[i]:data_x_min[i] + 5, k])
	

    # just for curiosity, check the consistency along the x axis, for this, we will average over the full y axis
    os_x_mean = np.zeros((N_os * nbins))
    os_x_sstd = np.zeros((N_os * nbins))
    for i_x in range(N_os * nbins):
	    # the sub-array of the overscan region
	    os_data =  (images[:, N_x + i_x ] )  # note: the first index is y-axis, the second axis is x
	    cn_x[i_x] = i_x + N_x # used in plotting
	    os_x_mean[i_x] =  np.mean(os_data)   #  calculate the mean for the two overscan regions
	    # sample standard deviation
	    os_x_sstd[i_x] =  (sts.stdev(os_data.flatten()))


    # the left and right half of the images from two amplifiers
    net_l = net[:,data_x_min[0]:data_x_max[0],k].flatten()
    net_r = net[:,data_x_min[1]:data_x_max[1],k].flatten()
    #if DEBUG:
       #print ('left mean and std: ', np.mean(net_l), sts.stdev(net_l.flatten()))
       #print ('right mean and std: ', np.mean(net_r), sts.stdev(net_r.flatten()))




    # plot histogram of mean and std
    fig, axes = plt.subplots(2,2, sharey='row', sharex='col')

    axes[0,0].plot(os_mean, cn_y)
    axes[0,0].set_title('overscan mean over 32 pxl')
    axes[0,0].grid(True)
    # toggle on grid
    plt.grid(which='both', axis='both', linestyle='-') 
    #axes.grid(color='r', linestyle='-', linewidth=2)
    axes[0,1].plot(os_sstd, cn_y)
    axes[0,1].set_title('overscan sample stdev')
    axes[0,1].grid(True)
    #ax3.plot(os_pstd, y)
    #mks.MarkerStyle('.')
    axes[1,0].plot(os_x_mean, cn_x)
    axes[1,0].set_title('mean over  4136 pxl')
    axes[1,0].grid(True)
    axes[1,1].plot(os_x_sstd, cn_x)
    axes[1,1].set_title('sstdev over 4136 pxl')
    axes[1,1].grid(True)

    plt.savefig(fig_out, orientation='landscape')
    #if DEBUG: 
       #plt.show()


    # create a new image file with image data = overscan
    hdu_os = fits.PrimaryHDU(overscan)
    hdu_os.writeto(file_os, overwrite='True')

    # create a new image file with image data = input - overscan
    hdu_net = fits.PrimaryHDU(net[:,:,k])
    hdu_net.writeto(file_net, overwrite='True')

# histogram the data after overscan subtraction
    fig2, axes2 = plt.subplots(2,3)
    axes2[1,0].hist(overscan.flatten(), bins=50)
    axes2[1,0].grid(True)
    axes2[0,0].set_title('32 x-pxls OS mean')
    axes2[0,0].plot(os_mean, cn_y)
    axes2[0,0].grid(True)
    # the hist of the left half image 
    axes2[0,1].hist(net_l, bins=50)
    axes2[0,1].grid(True)
    axes2[0,1].set_title('data (L)- OS')
    axes2[0,1].set_yscale('log')
    axes2[1,1].hist(net_l.flatten(), bins=50, range=[-100,100])
    axes2[1,1].grid(True)
    axes2[1,1].set_yscale('log')
    # the hist of the right half image 
    axes2[0,2].hist(net_r, bins=50)
    axes2[0,2].grid(True)
    axes2[0,2].set_title('data (R) - OS')
    axes2[0,2].set_yscale('log')
    axes2[1,2].hist(net_l.flatten(), bins=50, range=[-100,100])
    axes2[1,2].grid(True)
    axes2[1,2].set_yscale('log')
    plt.savefig(his_out, orientation='landscape')
    #plt.show()
    #if DEBUG:
    #   break

# find the median from net[0-5] = image[0-5] - OS
median = np.median(net, axis = 2) # ? along the last?? axis, which will be over the 5 images

if DEBUG: 
   print ('median shape', np.shape(median))
   print ('net[:,:,0] shape', np.shape(net[:,:,0]))
   print ('net shape', np.shape(net))
   #print ('median mu and sigma: ', np.mean(median), sts.stdev(median.flatten()))

for k in range(N_t):
# subtract bias for input data
    #real[:,:,k] = net[:,:,k] - median
    for i_x in range(N_x):
       for j_y in range(N_y):
           real[j_y,i_x,k] = net[j_y,i_x,k] - median[j_y,i_x]
    if DEBUG:
       print ('k = ', k)
       print (real[0,0,k], net[0,0,k] - median[0,0])
       print (real[0,1,k], net[0,1,k] - median[0,1])
       print (real[1,0,k], net[1,0,k] - median[1,0])
       #print ('real mean and std: ',k,  np.mean(real[:,:,k]), sts.stdev(real[:,:,k].flatten()))

# histogram the data after overscan subtraction
    data_net  =  net[:,:,k].flatten()
    data_real = real[:,:,k].flatten()
    fig3, axes3 = plt.subplots(2,3, sharey='row')
    # the hist of the net bias median
    axes3[0,0].hist(median.flatten(),bins=80, range=[-40,40])
    axes3[0,0].grid(True)
    axes3[0,0].set_title('median (raw - OS)')
    axes3[1,0].hist(median.flatten(), bins=120, range=[-30,30])
    axes3[1,0].grid(True)
    #axes3[1,0].set_yscale('log')
    # his of net = data - OS
    axes3[0,1].set_title('raw - OS')
    axes3[0,1].hist(data_net, bins=50)
    axes3[0,1].grid(True)
    axes3[0,1].set_yscale('log')
    axes3[1,1].hist(data_net, bins=120, range=[-30,30]) # zoom in
    axes3[1,1].grid(True)
    #axes3[1,1].set_yscale('log')
    # the hist of the real = data - OS - median
    axes3[0,2].hist(data_real, bins=50)
    axes3[0,2].grid(True)
    axes3[0,2].set_title('raw - OS - median')
    axes3[0,2].set_yscale('log')
    axes3[1,2].hist(data_real, bins=120, range=[-30,30])
    axes3[1,2].grid(True)
    #axes3[1,2].set_yscale('log')
    plt.savefig(his_real_out[k], orientation='landscape')
    #plt.show()

    # save to fits file
    hdu_real = fits.PrimaryHDU(real[:,:,k])
    hdu_real.writeto(file_real[k], overwrite='True')

# create a new fits file with image data = median
hdu_median = fits.PrimaryHDU(median)
hdu_median.writeto(file_median, overwrite='True')
