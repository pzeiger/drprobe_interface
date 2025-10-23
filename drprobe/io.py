# -*- coding: utf-8 -*-
"""
Created on Wed Oct  22 22:29:38 2025

@author: Paul Zeiger (pzeiger)
"""

import os
import glob
import time


def _from_bin(fname, shape, space, dtype):
    
    # We make sure that wav file is correctly written
    expected_size = shape[0] * shape[1] * dtype(1.0).nbytes
    while os.path.getsize(fname) != expected_size:
        time.sleep(1)
        print('expected size != size on disk:', 
              expected_size, os.path.getsize(fname))
    
    # shape[::-1] is needed as DrProbe saves the values of a MxN array in 
    # the following fashion:
    # 
    # a_11, a_21, ... a_M1, a_12, ..., a_M2, a12, ..., a1N, a2N, ..., aMN
    # 
    # and we want to make the following MxN array from it (x-axis is the
    # first, y- the second index):
    #
    # --                           --
    # | a_11 a_12  .   .   .   a_1N |
    # | a_21 a_22  .   .   .   a_2N |
    # |  .    .    .   .   .    .   |
    # |  .    .    .   .   .    .   |
    # |  .    .    .   .   .    .   |
    # | a_M1 a_M2  .   .   .   a_MN |
    # --                           --
    # 
    # 
    # 
    n2 = np.array(shape[::-1]) >> 1
    tmpshape = [x for x in shape[::-1]]
    
    # read the binary file
    a = np.fromfile(str_name, dtype=dtype).reshape(tmpshape)
    
    if space == 'reciprocal':
        # get the central beam to the center of the pattern
        a = np.roll(a, n2, axis=(0,1))  
    
    # We return the transpose, since otherwise we would get an array of shape (ny, nx)
    return a.T
    


def _to_bin(fname, array, dtype=np.single):
    """ Write array to binary file.
    """
    p = a.T
    if space == 'reciprocal':
        # get the central beam to the corner of the pattern
        n = np.array(p.shape) >> 1
        p = np.roll(p, np.array(p.shape)-n, axis=(0,1))
    
    p.astype(dtype).reshape(-1).tofile(fname)
    return



def load_dp(fname, shape, dtype=np.single):
    """ Load diffraction pattern.
    """
    return _from_bin(fname, shape, 'reciprocal', dtype)



def load_wav(fname, shape, dtype=np.csingle):
    """ Wave file.
    """
    return _from_bin(fname, shape, 'reciprocal', dtype)



def load_pot(fname, shape, dtype=np.single):
    """ Load real space potential.
    """
    return _from_bin(fname, shape, 'real', dtype)



def write_dp(fname, array, dtype=np.single):
    """ Write diffraction pattern to disk.
    """
    _to_bin(fname, array, 'reciprocal', dtype)



def write_wav(fname, array, dtype=np.csingle):
    """ Write wave to disk.
    """
    _to_bin(fname, array, 'reciprocal', dtype)


