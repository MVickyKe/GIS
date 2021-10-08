import os
import numpy as np
import pandas as pd
import xarray as xr
#import matplotlib.pyplot as plt
#import rioxarray as rio
#import seaborn as sns
#import geopandas as gpd
#import earthpy as et

### 1. Load NetCDF files
nc_file_prob = xr.open_dataset('/Users/keke/Desktop/GIS/prob_lower_tercile_MJJA2021_20210515.nc')
nc_file_ens = xr.open_dataset('/Users/keke/Desktop/GIS/ens_mean_wrsi_MJJA2021_20210515.nc')

### 2. View xarray object
# print(nc_file_ens)

# set Latitude and Longitute list
lat_lst = nc_file_prob["__xarray_dataarray_variable__"]["latitude"].values[:]
lon_lst = nc_file_prob["__xarray_dataarray_variable__"]["longitude"].values[:]
# print(lat_lst)

# transform the xarray value to match the real geographical outlook 
value_prob = np.flip(nc_file_prob['__xarray_dataarray_variable__'].T)
value_ens = np.flip(nc_file_ens['__xarray_dataarray_variable__'].T)

# print(value_ens)

### 3. Assign score for each file

# create "to_score" function 
def to_score(df,score_ruler,score_number):
    #define empty list to save score converting value
    final_score_list = []
    #based on the score values set above, convert the existing dataframe values to score values
    for k in range(0,len(lat_lst)):
        for j in df[k]:
            if pd.isna(j) == True:
                final_score_list.append(j)
            else:
                for i in range(1,len(score_ruler)):
                    if j >= score_ruler[i-1]:
                        if j < score_ruler[i]:
                            final_score_list.append(float(score_number[i-1]))
    #conver the output type from list to dataframe                      
    df_score_1 = np.reshape(final_score_list, (len(lat_lst), len(lon_lst)))
    #transform dataframe
    df_score_2 = []
    for i in df_score_1:
        a_lst = i[::-1]
        df_score_2.append(a_lst)
    #add columns and index for the dataframe to longitute and latitude
    final_score_df = pd.DataFrame(df_score_2,columns=lon_lst,index=lat_lst[::-1])
    #output the dataframe
    return(final_score_df)

### 4. Apply the datasets with to_score() function to convert data to score

# Set score range for value_ens dataset
# *********** change score **************
score = ["",'E','D','C','B','A']
score_ruler_1 = [0.00001,60,70,80,90,100]
score_number_1 = [1,2,3,4,5]

score_value_ens = to_score(value_ens,score_ruler_1,score_number_1)

# Set score range for value_prob dataset
# *********** change score **************
score = ["",'A','B','C']
score_ruler_2 = [0.00001,0.3,0.6,1]
score_number_2 = [3,2,1]

score_value_prob = to_score(value_prob,score_ruler_2,score_number_2)

### 5. Creat final drought score dataframe. 
# Multiply scores from two datasets together to get the final score

# Initial an empty list to store the converted value
drought_score_lst = []

# Use loop to multiply each value in the two datasets accordingly
for i in lat_lst[::-1]:
    for j in lon_lst:
        score = score_value_ens[j][i]*score_value_prob[j][i]
        drought_score_lst.append(score)

# Reshape list to dataframe
score_drought = np.reshape(drought_score_lst,(len(lat_lst), len(lon_lst)))
#final_score_drought = pd.DataFrame(score_drought,columns=lon_lst,index=lat_lst[::-1])

### 6. Set xarray properties
value = xr.DataArray(score_drought, [("latitude", lat_lst[::-1]),("longitude",lon_lst )])
value = value.rio.set_spatial_dims('longitude','latitude')
value.rio.crs
value.rio.set_crs("epsg:4326")


### 7. Convert to geotiff, then output the file
value.rio.to_raster(r"Drought Score Prediction_Ghana_MJJA2021.tiff")
