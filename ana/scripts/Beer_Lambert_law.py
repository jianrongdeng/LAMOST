"""
=======================================
Beer_Lambert Law
=======================================

*By: Jianrong Deng 20170518 
-------------------
Flux_out = Flux_in * pow(e, - rho * mass_attenuation_length_coefficient * material_thickness)),
where: 
	rho: number density of scattering centers (in g/cm^3)
	mass attenuation coefficient: total cross-section (in cm^2/g)
	material_thinkness: in cm
"""

##############################################################################
# LAMOST pixel size 12 um x 12 um
#        pixel thickness, not sure, assume 200 um for now  JD--TODO
# rho_Si = 2.33 g/cm^3
import math

pixel_thickness  = 200 * pow(10,-4)     # in cm
rho_Si = 2.33        # in g/cm^3
mass_attenuation_coefficient= 6.4 * pow(10, -2)     # for 1MeV photon in Si, in cm^2/g
flux_out_over_in = math.exp(- rho_Si * mass_attenuation_coefficient * pixel_thickness)

print('Flux_out / Flux_in = ', "{:%}".format(flux_out_over_in))

