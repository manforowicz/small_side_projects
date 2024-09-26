import os
import sys
from PIL import Image, ImageOps
import numpy as np
#from matplotlib import pyplot as plt

def normalize(arr):
	#Stretches the image contrast between black and full bright
	minval = np.percentile(arr, 0.1)
	maxval = np.percentile(arr, 99.9)
	arr = (arr - minval) * 255/(maxval-minval)
	arr = np.clip(arr, 0, 255)
	return arr
	
def hist_norm(x, bin_edges, quantiles, inplace=False):


    bin_edges = np.atleast_1d(bin_edges)
    quantiles = np.atleast_1d(quantiles)

    if bin_edges.shape[0] != quantiles.shape[0]:
        raise ValueError('# bin edges does not match number of quantiles')

    if not inplace:
        x = x.copy()
    oldshape = x.shape
    pix = x.ravel()

    pix_vals, bin_idx, counts = np.unique(pix, return_inverse=True,
                                          return_counts=True)

    ecdf = np.cumsum(counts).astype(np.float64)
    ecdf /= ecdf[-1]


    curr_edges = pix_vals[ecdf.searchsorted(quantiles)]

    diff = bin_edges - curr_edges


    pix_delta = np.interp(pix_vals, curr_edges, diff)

    pix += pix_delta[bin_idx].astype(np.uint8)

    return pix.reshape(oldshape)



def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w



names = ["Beach.jpg"]
for name in names:

		im = Image.open(name).convert('RGB')
		im = ImageOps.exif_transpose(im)
		arr = np.asarray(im)
		
		arr = moving_average(arr,(4,4,4,4,4,4))

		name = name.split('.')[-2]+"_b.jpg"
		im = Image.fromarray(arr.astype(np.uint8))
		im.save(name,quality=90,subsampling=0)
		


print('Finished')
