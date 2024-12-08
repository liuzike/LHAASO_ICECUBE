## A search for the neutrino signals from the LHAASO and H.E.S.S. gamma-ray sources

This repository contains the code used to perform the analysis described in the paper "A search for the neutrino signals from the LHAASO and H.E.S.S. gamma-ray sources" . The code is written in Python 3.8 and uses the following packages: numpy, scipy, matplotlib, pandas, numba, multiprocessing.

### **Description of the code**

The repository is organized as follows:

    - core
    - data
    - outputs
    - task4k_single_analysis.ipynb : an correlation  analysis between single gamma-ray source(Separated into WCDA-H.E.S.S. and KM2A-H.E.S.S. lists) and IceCube track events
    - task4k_stacking_analysis1_1.ipynb: constraints on neutrino flux from the LHASSO-WCDA-HESS sources based on  stacking analysis under the flux weighting scheme.
    - task4k_stacking_analysis1.ipynb: constraints on neutrino flux from the LHASSO-WCDA-HESS sources based on  stacking analysis under the uniform weighting scheme.
    - task4k_stacking_analysis2.ipynb: constraints on neutrino flux from the LHASSO-KM2A-HESS sources based on  stacking analysis under the uniform weighting scheme.
    - task4k_stacking_analysis2_1.ipynb: constraints on neutrino flux from the LHASSO-KM2A-HESS sources based on  stacking analysis under the flux weighting scheme.


#### **core**

The core/ directory contains the following files:

- download_IC.py : downloads the IceCube neutrino data package and saves it in data/icecube_10year_ps

- stacking_analysis.py : defines the functions used to calculate the Test statistic, and the signal flux model and other miscellaneous functions used in the analysis 

- req_arrays.py : Stores the required data in the form of numpy arrays for faster and easier computation

- readfiles.py : Reads and refines the data from the files and stores them in the form of panda.Dataframes

- signal_bag.py : defines the functions used to compute the Signal and Background PDF in the analysis 

- weights.py : (depercated) defines the functions used to compute the weights of pulsars for the analysis 

- plots.ipynb : plot the fig1 in this paper, a skymap describe all gamma-ray and neutrino events in our analysis


#### **data**

The data/ directory contains the data used in the analysis. The data are taken from the following sources:

- The IceCube neutrino data are taken from the public HESE and EHE data releases (http://icecube.wisc.edu/data-releases/20210126_PS-IC40-IC86_VII.zip). The data are stored in the data/icecube_10year_ps/ directory. The IceCube contains observations spanning over 10 years and is separated into 10 files, each corresponding to 1 year/1 IceCube season.


- The LHAASO data catalogue are taken from 2024 ApJS 271 25 and HESS catalogue (https://www.mpi-hd.mpg.de/hfm/HESS/pages/home/sources/).


#### **outputs**

The outputs/ , outputs3/ directory contains the results of the analysis in the form of images.


#### **Computational Complexity**

    

#### **Solution to the computational challenges**
- This is a very large number of values to compute. To overcome this challenge, we use the following techniques:

- Use the numba.njit package to speed up the computation. The numba package is used to compile the python code into machine code. 

- The integrals are evaluated using functions accelerated by numba.vectorize package and np.trapz, which is faster than scipy.quad or scipy.dblquad.

- Used numba.vectorize package to replace a for loop calling functions like `ns_sing_season`, `psr_wt_acc`. This reduce the computation time by a factor of 10.

- Used numba.prange to parallelize the computation. The prange package is used to run the code in parallel on multiple cores of the CPU. (Previously used python.multiprocessing. But it consumes a lot of memory and removes the numba acceleration so multiprocessing parts are depercated)

- Running the code normally requires ~ 2e12 calculations which take > 2 days of continuous computation.

- Using the above techniques, the computation time is reduced to ~ 2 hours.

