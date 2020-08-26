import os
import numpy as np
from astropy.io import fits
'''
Sersic distribution information
https://en.wikipedia.org/wiki/Sersic_profile#
'''

def initialize_params(k, shape):
    width = shape[0]
    height = shape[1]
    params = []

    for i in range(0, k):
        n = np.random.uniform(0, 100)
        b = 2 * (n ** (-1/3))
        a = np.random.uniform(0, 100)

        params.append([n, b, a])

    return params

def optim_params(params, data):
    pass

def optim_pixels(params, data):
    pass

def k_sersics(k, fits_fp):
    data = 0 
    with fits.open(fits_fp) as hdul:
        data = hdul[0].data

    shape = data.shape
    params = initialize_params(k, shape)
    
    

    pass
