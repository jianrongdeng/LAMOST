"""
=======================================
Calculate photon attenuation length in Si
=======================================

*By: Jianrong Deng 20170520 
-------------------
Input: 
	mass attenatuion coefficient: mass_att_coeff in cm^2/g
	rho: Si mass density, in g/cm^3
Output: attenuatuion length z (in cm), such that:
		z * mass_att_coeff * rho = 1
		fulx_out = flux_in * pow(e, -z * mass_att_coeff * rho) = flux_in / e

Reference/input data: http://physics.nist.gov/cgi-bin/Xcom/xcom3_1
		http://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html

"""

rho_Si = 2.33        # in g/cm^3
print('mass density of Si = ', rho_Si)

Energy_photon = [
pow(10, -3), 5*pow(10,-3), 
pow(10, -2), 1.5*pow(10,-2), 2*pow(10,-2),  5*pow(10,-2),  
pow(10, -1), 5*pow(10,-1),  
pow(10,  0), 5*pow(10, 0),  
pow(10, +1), 5*pow(10,+1),  
pow(10, +2), 5*pow(10,+2),  
pow(10, +3), 5*pow(10,+3),  
pow(10, +4), 5*pow(10,+4),  
pow(10, +5)
] 				# photon energy in MeV
#DB print('phton energy in Mev: ', Energy_photon)

# total attenuation with coherent scattering 
mass_att_coeff = [
1.570 * pow(10, +3), 2.451 * pow(10, +2),
3.388 * pow(10, +1), 1.034 * pow(10, +1), 4.630 * pow(10,  0), 4.385 * pow(10, -1),
1.835 * pow(10, -1), 8.748 * pow(10, -2),
6.361 * pow(10, -2), 2.967 * pow(10, -2),
2.462 * pow(10, -2), 2.522 * pow(10, -2),
2.764 * pow(10, -2), 3.229 * pow(10, -2),
3.344 * pow(10, -2), 3.469 * pow(10, -2),
3.493 * pow(10, -2), 3.512 * pow(10, -2),
3.517 * pow(10, -2)                      
]		# mass attenuation coefficient in cm^2/g
#DB print('total attenuation coefficient with coherent scattering, in cm^2/g = ', mass_att_coeff)

i = 0
att_len = []
for E_i in Energy_photon:
  #DB print('phton energy in Mev: ', E_i, Energy_photon[i]) # these two should be identical
  #DB print('total attenuation coefficient with coherent scattering, in cm^2/g = ', mass_att_coeff[i])
  z = 1/ (mass_att_coeff[i] * rho_Si)  # in cm
  #DB print('attenuation_length (cm) = ', z) 
  att_len.append([E_i, mass_att_coeff[i], z])
  i = i+1


print('reference: http://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html')
print('reference figure/tables: /Users/jdeng/baiduCloudDisk/MyFigures/LAMOST/photon_mass_attenuation_coefficient_on_Si.pdf')

print('photon Energy(MeV)', 'tot att coeff(cm^2/g)', 'att length(cm)')
for i in att_len:
   print ('{:2E},	{:2E},	{:2E}'.format(i[0], i[1], i[2]))


print('calculated using script: /Users/jdeng/百度云同步盘/LAMOST/ana/script/calculate_attenuation_length.py')
