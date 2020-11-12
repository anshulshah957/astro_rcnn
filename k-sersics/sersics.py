import os
import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit
from more_itertools import powerset

'''
Sersic distribution information
https://en.wikipedia.org/wiki/Sersic_profile#
'''

#TODO: Move back to not optmizing center values

#TODO: Search for good NUM_ITERS value
NUM_ITERS = 50

#TODO: Add object to make model aribtrary
def initialize_params(k, shape):
    width = shape[0]
    height = shape[1]
    params = []

    for i in range(0, k):
        n1 = np.random.uniform(0, 100)
        a1 = np.random.uniform(0, 100)
        n2 = np.random.uniform(0, 100)
        a2 = np.random.uniform(0, 100)
        center_x = np.random.uniform(0, width)
        center_y = np.random.uniform(0, height)
        params.append([center_x, center_y, n1, a1, n2, a2])

    return params

# TODO: Have generate seperate files or layers in TIF based on pixel partition
def write_output_partition(pixel_partition, data, fits_fp):
    data = 0 
    #TODO: Write all and seperate output file
    data = np.multiply(data, pixel_partition[0])


    #Change file to 0th partition
    with fits.open(fits_fp) as hdul:
        hdul[0] = data
        hdul.writeto(fits_fp, overwrite = True)

def optim_pixels(params, data, background_partition):
    shape = data.shape
    width = shape[0]
    height = shape[1]

    k = len(params)

    pixel_partition = np.zeros((k, width, height))
    print("Start")

    for ind_width in range(0, width):
        for ind_height in range(0, height):
            if (background_partition[ind_width][ind_height]):
                continue

            pred = [None] * k
            expected = data[ind_width][ind_height]

            for ind_sersic in range(0, k):
                center_x = params[ind_sersic][0]
                center_y = params[ind_sersic][1]
                n1 = params[ind_sersic][2]
                a1 = params[ind_sersic][3]
                n2 = params[ind_sersic][4]
                a2 = params[ind_sersic][5]

                pred_curr = sersic_curve([ind_width, ind_height], center_x, center_y, n1, a1, n2, a2)
                pred[ind_sersic] = pred_curr
            
            # Inefficient?
            all_combs = list(powerset(range(0, k)))
            optim_comb = None
            optim_err = None
            
            # Gets sersics combination with lowest error
            for comb in all_combs:
                curr_pred = sum([pred[ind] for ind in comb])
                curr_err = abs(expected - curr_pred)
            
                if optim_comb is None:
                    optim_comb = comb
                    optim_err = curr_err
                    continue

                if curr_err < optim_err:
                    optim_comb = comb
                    optim_err = curr_err

            total_pred = sum([pred[ind] for ind in comb])

            # Update Pixel Partition 
            for ind_sersic in range(0, k):
                if ind_sersic in optim_comb:
                    curr_val = float(pred[ind_sersic]) / float(total_pred)
                    pixel_partition[ind_sersic, ind_width, ind_height] = curr_val
                else:
                    pixel_partition[ind_sersic, ind_width, ind_height] = 0

    print("Done")

    return pixel_partition



def sersic_curve(x, center_x, center_y, n1, a1, n2, a2):
    center = np.asarray([center_x, center_y])
    r = np.linalg.norm(center - x)

    b1 = 2 * (n1 ** (-1/3))
    b2 = 2 * (n2 ** (-1/3))

    y1 = a1 * (np.exp(-b1 * r * (n1 ** (-1))))
    y2 = a2 * (np.exp(-b2 * r * (n2 ** (-1))))
    return y1+y2

# TODO: Use center_x and center_y from mask, and do not change
# TODO: Why is the partition error occuring here now
def optim_params(initial_params, pixel_partition, data):
    shape = pixel_partition.shape
    k = shape[0]
    width = shape[1]
    height = shape[2]
    params = []
    
    for i in range(0, k):
        curr_partition = pixel_partition[i]
        curr_data = np.multiply(curr_partition, data)
        y_data = curr_data.flatten()
        x_data = []
        
        for a in range(0, width):
            for b in range(0, height):
                x_data.append([a ,b])

        x_data = np.asarray(x_data)
        
        # Curve fit works better currently --> Why?
        params_i = curve_fit(sersic_curve, x_data, y_data, initial_params[i])
        params.append(params_i[0])
    
    return params


def k_sersics(k, fits_fp, num_iters = None):
    data = 0 
    with fits.open(fits_fp) as hdul:
        data = hdul[0].data

    if not num_iters:
        num_iters = NUM_ITERS

    shape = data.shape
    width = shape[0]
    height = shape[1]
    params = initialize_params(k, shape)

    # Replace with mask background partition
    background_partition = np.zeros((width, height))

    for i in range(0, num_iters):
        pixel_partition = optim_pixels(params, data, background_partition)
        params = optim_params(params, pixel_partition, data)

    return params



if __name__ == "__main__":
    print(k_sersics(1, "test_1.fits"))

