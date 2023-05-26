#this file is responsible for converting tif files into the data format used by keras
import pandas as pd
import numpy as np
from libtiff import TIFF
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
from tqdm import tqdm

#global variables
month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
#filepaths
elevation_path = 'data_sources/wc2.1_2.5m_elev.tif'
precipitation_path = 'data_sources/wc2.1_2.5m_prec/wc2.1_2.5m_prec_'


def testing():
    sea_list,geo_df = extract_coordinates(elevation_path) #extract geographic coordinates
    print(geo_df) #debug    
    precipitation_df = extract_precipitation_data(sea_list,precipitation_path)
    print(precipitation_df) #debug
    
def extract_precipitation_data(sea_list,precipitation_filepath):
    precipitation_df = extract_data_by_month(sea_list,precipitation_filepath,'precipitation')
    #max = precipitation_df.max()
    #min = precipitation_df.min()
    #mean = precipitation_df.mean()
    #print('max = ',max,' min = ',min,' mean = ',mean)
    #max precipitation seems to be 2768 mm per month. Scale so 0=0, 3000mm=1
    precipitation_df = precipitation_df/3000
    return precipitation_df



def extract_data_by_month(sea_list,path,data_name):
    print('extracting ',data_name,' data')
    #lists_data = []
    df = pd.DataFrame()
    #lists_names = []
    for month in range(1,13):
        month_name = month_names[month-1]
        print('for ',month_name)
        month_number = str(month)
        if(len(month_number)==1):
            month_number = "0" + month_number
        file_path = path + month_number + ".tif"
        tiff_array = Image.open(file_path) #load the tiff image file
        np_array = np.array(tiff_array) #convert to a numpy array
        np_array_height = np_array.shape[0] #total height of the array (latitude)
        np_array_width = np_array.shape[1] #total length of the array (longitude)
        sea_list_counter = 0
        list_data = []
        for i in tqdm(range(np_array_height)):
            for j in range(np_array_width):
                if sea_list[sea_list_counter]==True: #sea tile
                    sea_list_counter = sea_list_counter + 1
                    continue #we don't extract data from sea tiles in this model
                else:
                    sea_list_counter = sea_list_counter + 1
                    data = np_array[i][j]
                    list_data.append(float(data)) #explicit conversion to int/float needed for speed as otherwise data is stored in list as numpy array
        new_data_name = data_name + '_' + month_name
        #lists_data.append(list_data)
        df[new_data_name] = list_data
    print('all months finished, adding to dataframe')
    return df

    
                        



        
        

    

#extract latitude, longitude and whether it is a sea tile from a tif file representing elevation
def extract_coordinates(elevation_filepath):
    tiff_array = Image.open(elevation_filepath) #load the tiff image file
    #print("tiff array shape ",tiff_array.size, " type ",type(tiff_array))
    np_array = np.array(tiff_array) #convert to a numpy array
    #print("np array shape ",np_array.shape, " type ",type(np_array))
    np_array_height = np_array.shape[0] #total height of the array (latitude)
    np_array_width = np_array.shape[1] #total length of the array (longitude)
    sea_list = [] #list of boolean values, false=not sea, true=sea. Same length as flattened array. Same access order as this functions extraction code
    latitude_list = [] #latitude list for non-sea tiles
    longitude_list = [] #longitude list for non-sea tiles
    elevation_list = [] #elevation list for non-sea tiles
    #extraction code
    print('extracting geographic data, processing latitude by latitude')
    for i in tqdm(range(np_array_height)):
        latitude = 1-(i/(np_array_height/2)) #latitude will be a float between 1 (for 90 north) and -1 (for 90 south)
        for j in range(np_array_width):
            longitude = 1-(j/(np_array_width/2)) #longitude will be a float between 1 (for max west) and -1 (for max east)
            elevation = np_array[i][j] #extract the elevation
            if(elevation==-32768):#this elevation indicates a sea tile
                sea_list.append(True)
            else:
                sea_list.append(False)
                elevation = elevation/10000 #elevation is a float between -1 and 1 representing -10000 to 10000 metres
                latitude_list.append(latitude)
                longitude_list.append(longitude)
                elevation_list.append(elevation)
    #convert to dataframe
    print("converting to dataframe")
    geo_df = pd.DataFrame(list(zip(latitude_list,longitude_list,elevation_list)),columns=["Latitude","Longitude","Elevation"])
    #now export the data
    return sea_list,geo_df

if __name__ == "__main__":
    testing()