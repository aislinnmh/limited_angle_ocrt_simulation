This repository contains Python code to 1) simulate multi-angle optical coherence tomography (OCT) of a polystyrene bead phantom, 2) create multi-angle OCT datasets of varied angular sampling extents and densities, and 3) run optical coherence refraction tomography (OCRT) experiments on these datasets. It also contains MATLAB code to assist with data analysis of these experiments. The _ex vivo_ mouse vas deferens data used in these experiments can be found at https://doi.org/10.6084/m9.figshare.8297138 in the file mouse_vas_deferens1.mat [1].

This repository also contains code to implement the 2D OCRT algorithm published by Zhou et al. in 2019 in the files run_ocrt.ipynb and ocrt.py [1]. These files have been updated to run with TensorFlow 2 and adjusted for the experiments in this repository. The original OCRT code and README.md for that project can be found at https://github.com/kevinczhou/optical-coherence-refraction-tomography. 

The code may require >40 GB RAM and depends on the following libraries:
- tensorflow (the CPU version is sufficient)
- numpy
- scipy
- opencv
- matplotlib
- jupyter
- os
- random
  
The data analysis requires the MATLAB Curve Fitting toolbox.

[1] Zhou, K. C., Qian, R., Degan, S., Farsiu, S., & Izatt, J. A. Optical coherence refraction tomography. *Nature Photonics*, 13(11), 794-802 (2019).
