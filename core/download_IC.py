############################################################################################################################
# This code downloads the 2008-2018 data release file from the IceCube website

# The data is stored in the data folder
############################################################################################################################

import requests
import os
import wget

from zipfile import ZipFile
current_dir=os.getcwd()
data_dir=os.path.abspath(os.path.join(current_dir,".."))+'/data/'

if 'icecube_10year_ps' not in os.listdir(data_dir) or os.listdir(data_dir + 'icecube_10year_ps') == []:
#    url = 'http://icecube.wisc.edu/data-releases/20210126_PS-IC40-IC86_VII.zip'
#    wget.download(url, data_dir + 'data.zip')

#    r = requests.get(url, allow_redirects=True)

   
   with ZipFile(data_dir + 'data.zip','r') as zipObj:
   # Extract all the contents of zip file in current directory
      zipObj.extractall(data_dir)


   # Delete the zip file
   os.remove(data_dir + 'data.zip')

   print('Data downloaded successfully')

else:
   pass

