import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rio
import seaborn as sns
import geopandas as gpd
import earthpy as et

df_smforecast = pd.read_csv("/Users/keke/Desktop/extract_point/sm_forecast_MJJA_score_number.csv",index_col = 0)
df_lowprob = pd.read_csv("/Users/keke/Desktop/extract_point/sm_prob_lower_tercile_MJJA_score_number.csv",index_col = 0)

# 2. set latitude and longitude range
lat_start = -3.25
lat_end = 1.5
lon_start = 4.25
lon_end = 11.25

#set step value
step = 0.25

#create latitude and longitude list
lat_list = np.arange(lat_start,lat_end,step)
lon_list = np.arange(lon_end,lon_start,-step)

final_score_lst = []
for i in lat_list:
    for j in lon_list:
        score = df_smforecast[str(i)][j]*df_lowprob[str(i)][j]
        final_score_lst.append(score)
final_score_lst


final_score_matrix = np.reshape(final_score_lst, (len(lat_list), len(lon_list))).T
#print(final_score_matrix)

value = xr.DataArray(final_score_matrix, [("latitude", lon_list),("longitude",lat_list )])


value = value.rio.set_spatial_dims('longitude','latitude')
value.rio.crs
value.rio.set_crs("epsg:4326")

#convert from netcdf to geotiff
value.rio.to_raster(r"score_raster.tiff")
