## A search for the neutrino signals from the LHAASO and H.E.S.S. gamma-ray sources

This repository contains the code used to perform the analysis described in the paper "A search for the neutrino signals from the LHAASO and H.E.S.S. gamma-ray sources" . The code is written in Python 3.8 and uses the following packages: numpy, scipy, matplotlib, pandas, numba, multiprocessing.

### **Description of the code**

The repository is organized as follows:

    - core
    - data
    - outputs
    - task4k_single_analysis.ipynb : an correlation  analysis between single gamma-ray source(Separated into WCDA-H.E.S.S. and KM2A-H.E.S.S. lists) and IceCube track events
    - task4k_stacking_analysis1_1.ipynb: constraints on neutrino flux from the LHASSO-WCDA-HESS sources based on  stacking analysis under the uniform weighting scheme.
    - task4k_stacking_analysis1_2.ipynb: constraints on neutrino flux from the LHASSO-KM2A-HESS sources based on  stacking analysis under the flux weighting scheme.


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

The outputs/ directory contains the results of the analysis in the form of images.


#### **Computational Complexity**

The signal PDF requires heavy computation which consists:

- Angles between 2374 pulsars * 1134450 neutrinos = 269,500,850 values.
- $\omega_{acc}$ for 2374 pulsars. Each pulsar is attributed a weight $\omega_{acc}$ which is proportional to the declination and detector effective area. It is given by:
    
    $\omega_{acc,j} = T \times \int A_{eff}(E_{\nu}, \delta_j)E_{\nu}^{\Gamma} dE_{\nu}$

    where $T$ is the livetime of the detector, $A_{eff}$ is the effective area of the detector, $\Gamma$ is the spectral index of the neutrino flux, and $\delta_j$ is the declination of the $j^{th}$ pulsar. The effective area of the detector is a function of the neutrino energy and the declination of the source. The effective area is calculated for 1134450 neutrinos and 2374 pulsars.

- The above integral is calculated using np.trapz for 1e7 energies for each of the 10 seasons of the IceCube and for 3 different spectral indices for 2374 pulsars. 
<!-- This requires computing 2374 * 1e7 * 30 = 7.122e11 values.  -->

- The no.of signal events for each pulsar indexed by $j$ is given by: 

    $\hat{n}_{s_j} =  T \times \intop A_{eff}(E_{\nu}, \delta_j)\dfrac{dF}{dE_{\nu}}dE_{\nu}$

    $T$, $A_{eff}$, and $\delta_j$ are the same as above. $\dfrac{dF}{dE_{\nu}}$ is the expected neutrino spectrum from the source and can be modelled using a power-law as follows:

    $\dfrac{dF}{dE_{\nu}} = \phi_0  \left( \dfrac{E_{\nu}}{100 \text{ TeV}}\right)^{\Gamma}$

    where  $\phi_0$ is the flux normalization and $\Gamma$ is the spectral index. Each $\hat{n}_s$ is calculated for 1e7 energies for each of the 10 seasons of the IceCube and for 3 different spectral indices for 2374 pulsars. 
    <!-- This requires computing 2374 * 1e7 * 30 = 7.122e11 values. -->

- The above two integrals are calculated using np.trapz for 1e7 energies for each of the 10 seasons of the IceCube and for 3 different spectral indices for 2374 pulsars. This requires computing 2374 * 1e7 * 30 = 7.122e11 values.

Then the stacked Signal PDF for each neutrino $i$ is calculated by taking the weighted sum over the individual pulsars with three different weight models.

The Likelihood of $\hat{n}_s$ signal events is given by: 

    $\mathcal{L}(n_s) = \prod_i \frac{n_s}{N} S_i + (1-\frac{n_s}{N}) B_i$

   where $N$ is the total number of neutrinos, $S_i$ is the signal PDF for the $i^{th}$ neutrino, and $B_i$ is the background PDF for the $i^{th}$ neutrino. The background PDF is the no.of neutrinos within 5$^\circ$ angular cone of the $i^{th}$ neutrino. The background PDF is calculated for 1134450 neutrinos. The Likelihood is calculated for 3 different spectral indices. This requires 1134450 * 3 = 7.122e11 values.

We then easily calculate upper limits by using scipy.interp1d as the no.of values required are less
    

#### **Solution to the computational challenges**
- This is a very large number of values to compute. To overcome this challenge, we use the following techniques:

- Use the numba.njit package to speed up the computation. The numba package is used to compile the python code into machine code. 

- The integrals are evaluated using functions accelerated by numba.vectorize package and np.trapz, which is faster than scipy.quad or scipy.dblquad.

- Used numba.vectorize package to replace a for loop calling functions like `ns_sing_season`, `psr_wt_acc`. This reduce the computation time by a factor of 10.

- Used numba.prange to parallelize the computation. The prange package is used to run the code in parallel on multiple cores of the CPU. (Previously used python.multiprocessing. But it consumes a lot of memory and removes the numba acceleration so multiprocessing parts are depercated)

- Running the code normally requires ~ 2e12 calculations which take > 2 days of continuous computation.

- Using the above techniques, the computation time is reduced to ~ 2 hours.

