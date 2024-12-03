###########################################################################################################################
###########################################################################################################################
#                                                                                                                         #
# This file contains all the required arrays and variables for the task 4 of Project IceCube                              #
#                                                                                                                         #
#Data:                                                                                                                    #
#                                                                                                                         #
# icdata: The IceCube data                                                                                                #
#                                                                                                                         #
# uptdata: The UPT data                                                                                                   #
#                                                                                                                         #
# eadata: The Effective Area data                                                                                         #
#                                                                                                                         #
# mspdata: The MSP data                                                                                                   #
#                                                                                                                         #
#Vectors:                                                                                                                 #
#                                                                                                                         #
# msdec: The declination of the pulsars in the ATNF catalogue                                                             #
#                                                                                                                         #
# msra: The right ascension of the pulsars in the ATNF catalogue                                                          #
#                                                                                                                         #                                                                                                                        #
# icdec: The declination of the neutrinos in the IceCube data                                                             #
#                                                                                                                         #
# icra: The right ascension of the neutrinos in the IceCube data                                                          #
#                                                                                                                         #
# icang: The angular error of the neutrinos in the IceCube data                                                           #
#                                                                                                                         #
# iceng: The energy of the neutrinos in the IceCube data (in GeV)                                                         #
#                                                                                                                         #
# icwidths: The widths of the seasons in the IceCube data                                                                 #
#                                                                                                                         #
# ictimes: The times of the seasons in the IceCube data                                                                   #
#                                                                                                                         #
# icparts: The partitions of the IceCube data for each season                                                             #
#                                                                                                                         #
# upt_icparts: The partitions of the UPT data for each season                                                             #
#                                                                                                                         #
# t_upt: The detector uptime of the seasons from the uptime data                                                          #
#                                                                                                                         #
# log_e: The log10(E/GeV) values range as in all 'effectiveArea' files                                                    #
#                                                                                                                         #
# dec_nu: Set of Declination walls in all 'effectiveArea' files                                                           #
#                                                                                                                         #
# e_nu: The mid point of E_nu_min and E_nu_max as in all 'effectiveArea' files                                            #
#                                                                                                                         #
# de_nu: The difference of E_nu_min and E_nu_max as in all 'effectiveArea' files                                          #
#                                                                                                                         #
# earea: The effective area of the seasons in the effectiveArea data (in m^2)                                             #
#                                                                                                                         # 
# msdist: The distance of the pulsars in the ATNF catalogue (in kpc)                                                      #
#                                                                                                                         #
# mss1400: The flux at 1400 MHz of the pulsars in the ATNF catalogue (in mJy)                                             #
#                                                                                                                         #
###########################################################################################################################

# The arrays are stored in the form of numpy vectors

# The arrays and variables are used in the following files:

# ../core/req_arrays.py

# ../core/signal_bag.py

# ../core/stacking_analysis.py

# ../core/weights.py

# ../task4k_packed.ipynb

###########################################################################################################################
###########################################################################################################################

from core import read_files                     #Comment this line if you are using the CHIME data
# from core import readfiles_CHIME as readfiles   #Comment this line if you are using the ATNF data
import numpy as np
import os

all_data = read_files.Data(os.path.abspath(os.path.join(os.getcwd()))+'/data/')
icdata = all_data.icdata
uptdata = all_data.uptdata
eadata = all_data.eadata
mspdata = all_data.mspdata
lhsadata1=all_data.lhassodata1
lhsadata2=all_data.lhassodata2
icbtrack_data=all_data.icbtrackdata
hessdata=all_data.hessdata
all_data = []

#ICECUBE DATA VECTORS
icwidths = [int(i) for i in "0 36900 107011 93133 136244 112858 122541 127045 129311 123657 145750".split(' ')]
# ictimes = [float(i) for i in icdata['MJD[days]']]
icparts = [np.sum(icwidths[:i]) for i in range(1,len(icwidths)+1)]  #paritions of icdata for each season (IC40, IC59, IC79, IC86_I, IC86_II)

upt_icparts = icparts[:5]
upt_icparts.append(icparts[-1])
upstop_ttt = np.asfarray([uptdata[i]['MJD_stop[days]'].values[-1] for i in range(len(uptdata))], dtype=np.float64)
upstart_ttt = np.asfarray([uptdata[i]['MJD_start[days]'].values[0] for i in range(len(uptdata))], dtype=np.float64)
vec_uptparts = np.asarray(upt_icparts, dtype=np.int64)
upt_icparts = np.asarray(upt_icparts)
t_upt1 = np.asfarray([np.sum(uptdata[i]['MJD_stop[days]'].values-uptdata[i]['MJD_start[days]'].values) for i in
                       range(len(uptdata))], dtype=np.float64)*86400
t_upt = np.asarray([upstop_ttt[season] - upstart_ttt[season] for season in range(len(upstart_ttt))])*86400 #Convert days to seconds
#t_upt in seconds
icra = np.array([float(i) for i in icdata['RA[deg]']], dtype=np.float64)              #RA in degrees
icdec = np.array([float(i) for i in icdata['Dec[deg]']], dtype=np.float64)            #Dec in degrees
icang = np.array([float(i) for i in icdata['AngErr[deg]']], dtype=np.float64)         #AngErr in degrees
iceng=np.array([float(i) for i in icdata['log10(E/GeV)']])
log_e = np.round(np.arange(2, 10.2, 0.2), 2) #log10(E/GeV) values range as in all 'effectiveArea' files
earea = np.asfarray([eadata[i]['A_Eff[cm^2]'].values for i in range(len(eadata))])     #cm2
#dec_nu = Set of Declination walls in all 'effectiveArea' files
dec_nu = list(set(eadata[0]['Dec_nu_min[deg]'].values).union(set(eadata[0]['Dec_nu_max[deg]'].values)))

dec_nu.sort()
dec_nu = np.array(dec_nu)

e_nu_wall = np.asarray((10**log_e) * 1e9)

e_nu = ((10**(log_e[:-1])+ 10**(log_e[1:]))/2)*1e9          #E_nu in eV
de_nu = 1e9*(10**log_e[1:] - 10**log_e[:-1])                #dE_nu in eV

#ATNF PULSAR VECTORS

msra = np.array([float(i) for i in mspdata['RAJD'].values], dtype=np.float64)         #RAJD in degrees
msdec = np.asfarray([float(i) for i in mspdata['DECJD'].values], dtype=np.float64)       #DECJD in degrees
# msra = np.array([float(i) for i in mspdata['ra'].values], dtype=np.float64)         #RA CHIME in degrees
# msdec = np.array([float(i) for i in mspdata['dec'].values], dtype=np.float64)       #DEC CHIME in degrees
msdist=np.array([i for i in mspdata['DIST'].values], dtype=str)
msdist[np.where(msdist=='*')]='0.0'
msdist=np.float64(msdist)
msdist_dm=np.array([i for i in mspdata['DIST_DM'].values], dtype=str)
msdist_dm[np.where(msdist_dm=='*')]='0.0'
msdist_dm=np.float64(msdist_dm)
mss1400=np.array([i for i in mspdata['S1400'].values], dtype=str)
mss1400[np.where(mss1400=='*')]='0.0'
mss1400=np.float64(mss1400)
global p, lg, lnu
p = len(msra)
lg = 1 + len(icra) // p
lnu = len(icra)

deg2rad_var = np.pi/180
# icdata = []
# uptdata = []
# eadata = []
# mspdata = []
#LHSAAO SOURCE VECTOR
lhsaao1ra=np.asfarray([float(i) for i in lhsadata1['RA'].values], dtype=str)
lhsaao1name=[i for i in lhsadata1['Source_name'].values]
lhsaao1dec=np.asfarray([float(i) for i in lhsadata1['DEC'].values], dtype=str)
lhsaao1fnu=np.asfarray([float(i) for i in lhsadata1['N0'].values], dtype=str)
lhsaao1fnu_nor=lhsaao1fnu/np.sum(lhsaao1fnu)
lhsaao2ra=np.asfarray([float(i) for i in lhsadata2['RA'].values], dtype=str)
lhsaao2name=[i for i in lhsadata2['Source_name'].values]
lhsaao2dec=np.asfarray([float(i) for i in lhsadata2['DEC'].values], dtype=str)
lhsaao2fnu=np.asfarray([float(i) for i in lhsadata2['N0 '].values], dtype=str)
lhsaao2fnu_nor=lhsaao2fnu/np.sum(lhsaao2fnu)
global p1,p2
p1=len(lhsaao1ra)
p2=len(lhsaao2ra)
# All units check out:   eV, cm2, s, deg, GeV

#ICECUBE_TRACK SOURCE VECTOR
icetrackra=np.asfarray([float(i) for i in icbtrack_data['RA'].values], dtype=str)
icetrackdec=np.asfarray([float(i) for i in icbtrack_data['DEC'].values], dtype=str)
icetrackdeng=(np.asfarray([float(i) for i in icbtrack_data['DEC_ERR_PLUS'].values], dtype=str)+np.asfarray([float(i) for i in icbtrack_data['DEC_ERR_PLUS'].values], dtype=str))*0.5
icetracke=np.asfarray([float(i) for i in icbtrack_data['ENERGY'].values], dtype=str)


#HESS SOURCE VECTOR

hess_ra=np.asfarray([float(i) for i in hessdata['RA'].values], dtype=str)
hess_name=[i for i in hessdata['\xa0Name'].values]
hess_dec=np.asfarray([float(i) for i in hessdata['Decl'].values], dtype=str)
hessfnu=np.asfarray([float(i) for i in hessdata['Flux \xa0(max)\xa0[C.U.]'].values], dtype=str)

