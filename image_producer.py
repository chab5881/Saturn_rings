
from pyciss.ringcube import RingCube
import numpy as np
from matplotlib import pyplot as plt

import pyciss.ringcube

#
#
###Let's make a pipeline!
#
#

#All file names
from glob import glob
rawDir = glob("/cassini_ringsdata/db/N*")  #This leaves out the one directory with W*
rawDir = np.array(rawDir)

for i in np.arange(0,rawDir.size):
    rawDir[i] = rawDir[i][22:]


#Function for saving png files
def pngSave(filename):
    icube = RingCube(filename)
    idata = icube.img
    
    size = (idata.shape[0] - 55) / (55.8)
    
    fig = plt.figure(figsize=(size,size))
    extent_val = icube.extent
    min_, max_ = np.percentile(idata[~np.isnan(idata)], (1, 99))
    plt.imshow(idata, extent=extent_val, cmap='gray', vmin=min_, vmax=max_, interpolation='none', origin='lower', aspect='auto')
    plt.axis('off')
    plt.savefig('../pngFiles/' + filename + '_img.png', bbox_inches='tight')
    plt.close(fig)
    
    ifs = np.nanmedian(icube.img, axis=1)
    ifs = np.nan_to_num(ifs)
    ifs[ifs < 0] = 0
    
    fig = plt.figure(facecolor='white',figsize=(size,size))
    plt.plot(ifs, np.linspace(*icube.extent[2:], idata.shape[0]), color='black', lw=1.3)
    plt.axis('off')
    plt.savefig('../pngFiles/' + filename + '_plot.png', bbox_inches='tight')
    plt.close(fig)
    return


#Loop to save png files
import csv

errorFiles = np.array([])
for i in np.arange(0,rawDir.size):
    try:
        pngSave(rawDir[i])
    except:
        print(rawDir[i])
        errorFiles = np.append(errorFiles, rawDir[i])

with open('errorFiles.txt', 'w') as file_handler:
    for i in errorFiles:
        file_handler.write("{}\n".format(i))
