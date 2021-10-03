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
nc_file = xr.open_dataset('/Users/keke/Desktop/GIS/prob_lower_tercile_MJJA2021_20210515.nc')

#view xarray object
#print(nc_file)

#View latitude and longitude values
lat_lst = nc_file["__xarray_dataarray_variable__"]["latitude"].values[:]
lon_lst = nc_file["__xarray_dataarray_variable__"]["longitude"].values[:]
#print('latitude',lat_lst)
#print('longitude',lon_lst)


value = np.flip(nc_file['__xarray_dataarray_variable__'].T)
#print(value)

value = value.rio.set_spatial_dims('longitude','latitude')
value.rio.crs
value.rio.set_crs("epsg:4326")

#convert from netcdf to geotiff
value.rio.to_raster(r"to_raster.tiff")