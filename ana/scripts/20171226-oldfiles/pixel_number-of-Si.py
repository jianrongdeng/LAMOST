"""
=======================================
Calculate number of Si in a LAMOST pixel
=======================================

*By: Jianrong Deng 20170517 
-------------------
"""
##############################################################################
# LAMOST pixel size 12 um x 12 um
#        pixel thickness, not sure, assume 200 um for now  JD--TODO
# rho_Si = 2.33 g/cm^3
# 1 mol of 28Si = 28 gram
# A_Si = 28 
# N_A = 6.22 * 10^23 mol^{-1}: Avogadro constant 

pixel_size = 12 * 12 # in um^2
pixel_thick  = 200     # in um
rho_Si = 2.33        # in g/cm^3
N_A = 6.02 * pow(10,23) # Avogadro constant
A_Si = 28
pixel_weight = pixel_size * pixel_thick * pow(10, -4*3) * rho_Si # 1um = 10^-4 cm
pixel_N_Si = N_A / A_Si * pixel_weight 
print('number of Si atoms in one pixel:', "{:E}".format(pixel_N_Si))

