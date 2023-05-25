#this file is responsible for converting tif files into the data format used by keras
import pandas as pd
import numpy as np
from libtiff import TIFF
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt

#extract latitude, longitude and whether it is a sea tile from a tif file representing elevation
def extract_coordinates(elevation_filepath):
    tiff_array = Image.open(elevation_filepath) #load the tiff image file
    print("tiff array shape ",tiff_array.size, " type ",type(tiff_array))
    np_array = np.array(tiff_array) #convert to a numpy array

    



    





if __name__ == "__main__":
    extract_coordinates('data_sources/wc2.1_2.5m_elev.tif')