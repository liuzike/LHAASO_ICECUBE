# -*- coding: utf-8 -*-
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
all_data = read_files.Data(os.path.abspath(os.path.join(os.getcwd(),".."))+'/data/')
icdata = all_data.icdata
uptdata = all_data.uptdata
eadata = all_data.eadata
mspdata = all_data.mspdata
all_data = []
def _init():  # initialization
    global _global_dict
    _global_dict = {'msdec','msra','icdec','icra','icang','iceng','icwidths','ictimes','icparts','upt_icparts','t_upt',
                    'log_e','dec_nu','earea','msdist','mss1400'}

def set_value(key, value):
    #define global ICECUBE data var
    _global_dict['icwidths']=[int(i) for i in "0 36900 107011 93133 136244 112858 122541 127045 129311 123657 145750".split(' ')]
    _global_dict['icparts']=[np.sum(_global_dict['icwidths'][:i]) for i in range(1,len(_global_dict['icwidths'])+1)]
    _global_dict['upt_icparts']=_global_dict['icparts'][:5].append(_global_dict['icparts'][-1])
    _global_dict['upstop_ttt']=np.asfarray([uptdata[i]['MJD_stop[days]'].values[-1] for i in range(len(uptdata))], dtype=np.float64)
    _global_dict['icdec']=np.array([float(i) for i in icdata['Dec[deg]']], dtype=np.float64)
    _global_dict['icra']=np.array([float(i) for i in icdata['RA[deg]']], dtype=np.float64)
    _global_dict['icang']=np.array([float(i) for i in icdata['AngErr[deg]']], dtype=np.float64)
    _global_dict['iceng']=np.array([float(i) for i in icdata['log10(E/GeV)']])
    _global_dict['upstart_ttt']=np.asfarray([uptdata[i]['MJD_start[days]'].values[0] for i in range(len(uptdata))], dtype=np.float64)
    _global_dict['vec_uptparts']=np.asarray(_global_dict['upt_icparts'], dtype=np.int64)
    _global_dict['upt_icparts']=np.asarray[_global_dict['upt_icparts']]
    _global_dict['t_upt']=np.asarray([_global_dict['upstop_ttt'][season] - _global_dict['upstart_ttt'][season] for season in range(len(_global_dict['upstart_ttt']))])*86400
    _global_dict['log_e']=np.round(np.arange(2, 10.2, 0.2), 2) 
    _global_dict['earea']=np.asfarray([eadata[i]['A_Eff[cm^2]'].values for i in range(len(eadata))]) 
    _global_dict['dec_nu']=list(set(eadata[0]['Dec_nu_min[deg]'].values).union(set(eadata[0]['Dec_nu_max[deg]'].values)))
    _global_dict['dec_nu']=np.array(_global_dict['dec_nu'])
    _global_dict['dec_nu'].sort()
    _global_dict['dec_nu']= np.array(_global_dict['dec_nu'])
    _global_dict['e_nu_wall'] = np.asarray((10**_global_dict['log_e']) * 1e9)
    #define ANFT pulsar vector
    _global_dict['msdec'] = np.asfarray([float(i) for i in mspdata['DECJD'].values], dtype=np.float64)
    _global_dict['msra']=np.array([float(i) for i in mspdata['RAJD'].values], dtype=np.float64)
    _global_dict['mdist']=np.array([float(i) for i in mspdata['RAJD'].values], dtype=np.float64)

def get_value(key):
    try:
        return _global_dict[key]
    except:
        print('读取'+key+'失败\r\n')