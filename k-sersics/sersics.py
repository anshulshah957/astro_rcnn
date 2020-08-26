import os
import numpy as np
from astropy.io import fits
'''
Sersic distribution information
https://en.wikipedia.org/wiki/Sersic_profile#
'''

NUM_ITERS = 50
#TODO: add support for background partition

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

def optim_params(pixel_partition, data):
    shape = pixel_partition.shape
    k = shape[0]
    params = []
    
    for i in range(0, k):
        curr_partition = pixel_partition[i]
        curr_data = np.multiply(curr_partition, data)
        
        #TODO: extract radius information from curr_data
        #TODO: Use scipy curve_fit to fit to a sersic distribution with n and a values (b calculated from n)


def optim_pixels(params, data):
    pass

def k_sersics(k, fits_fp, num_iters = None):
    data = 0 
    with fits.open(fits_fp) as hdul:
        data = hdul[0].data

    if not num_iters:
        num_iters = NUM_ITERS

    shape = data.shape
    params = initialize_params(k, shape)
    pixel_partition = 0

    for i in range(0, num_iters):
        pixel_partition = optimize_pixels(params, data)
        params = optimize_params(pixel_partition, data)

    return params

