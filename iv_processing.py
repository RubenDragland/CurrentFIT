import numpy as np
import matplotlib.pyplot as plt

import os
import sys
import glob
import re
import pandas as pd

import scipy.stats as stats


def read_iv(path, folder, filename):

    full_path = os.path.join(path, folder, filename)
    df = pd.read_csv(full_path, sep=",", header=0)
    return df

def process_data(df, iterations, voltages):
    arr = df.to_numpy()
    arr_shaped = arr.reshape(arr.shape[0]//iterations, iterations, arr.shape[1])
    arr_median = np.median(arr_shaped, axis=1)
    
    arr_finished = np.reshape(arr_median, (arr_median.shape[0]//voltages, voltages , arr_median.shape[1])) #NOTE: Believe to be wrong. Correct for T-dependent data. 
    arr_finished = np.reshape(arr_finished, (-1, arr_finished.shape[1]//4, arr_finished.shape[2])) #TODO: Include options for how many to use. 
    
    return arr_finished

def process_sep_abs_iv(df, iterations, voltages):
    '''
    Processes the IV data by separating the absolute values of the median IV curve into four parts.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the IV data.
    iterations : int
        The number of iterations (repeats) in the IV data.
    voltages : int
        The number of voltage points in the IV data.
    Returns
    -------
    arr_finished : numpy.ndarray
        A 2D array containing the absolute values of the median IV curve, separated into four parts.
    '''
    arr = df.to_numpy()
    arr_shaped = arr.reshape(arr.shape[0]//iterations, iterations, arr.shape[1])
    arr_median = np.median(arr_shaped, axis=1) # NOTE!!! Works. 

    arr1 = np.abs(arr_median[:voltages//4 +1, 2:4])
    arr2 = np.abs(arr_median[voltages//4:voltages//2 + 1, 2:4])[::-1]
    arr3 = np.abs(arr_median[voltages//2:3*voltages//4 + 1, 2:4])
    indices = np.arange(3*voltages//4, voltages+1, 1)
    indices[-1] = 0
    arr4 = np.abs(arr_median[indices, 2:4])[::-1]

    arr_finished = np.stack((arr1, arr2, arr3, arr4), axis=0)

    return arr_finished

def process_series(stacked, add_on):
    arr = np.concatenate((stacked, add_on), axis=0)
    return arr

def create_dataset(files):
    pass#TODO.
    return

'''
Plan for data-loading. 
Each csv file is one IV curve.
Each IV curve has more repeats, but we filter noise by taking the median.
The full IV curve is then separated into four parts. Up from 0, down to zero, down to max negative, and back to 0. Settings for which indexes to include.

For high voltages, settings for how to filter the range of the IV curve. 
Also, more temperatures. Would be beneficial to include this as well because this is constant. Assume ionized carriers and hence ccd equal to ionized carriers and no T dependence. 

Maybe include all the data for each sample in each step. That or SGD which will prob be noisy. Start with one curve and add on later. 

'''