import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rio
import seaborn as sns
import geopandas as gpd
import earthpy as et


#load file
nc_file_prob = xr.open_dataset('/Users/keke/Desktop/GIS/prob_lower_tercile_MJJA2021_20210515.nc')
nc_file_ens = xr.open_dataset('/Users/keke/Desktop/GIS/ens_mean_wrsi_MJJA2021_20210515.nc')

#view xarray object
#print(nc_file_ens)

lat_lst = nc_file_prob["__xarray_dataarray_variable__"]["latitude"].values[:]
lon_lst = nc_file_prob["__xarray_dataarray_variable__"]["longitude"].values[:]

print(lat_lst)

value_prob = np.flip(nc_file_prob['__xarray_dataarray_variable__'].T)
value_ens = np.flip(nc_file_ens['__xarray_dataarray_variable__'].T)

#print(value_ens)



#xr.DataArray(np.arange(532).reshape(28, 19), [("latitude", lat_lst),("longitude",lon_lst)])
