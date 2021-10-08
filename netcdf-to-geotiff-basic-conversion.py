import os
import numpy as np
import pandas as pd
import xarray as xr
#import matplotlib.pyplot as plt
#import rioxarray as rio
#import seaborn as sns
#import geopandas as gpd
#import earthpy as et

# 1. Load netCDF file
nc_file = xr.open_dataset('/Users/keke/Desktop/GIS/prob_lower_tercile_MJJA2021_20210515.nc')

# 2. View netCDF file
#print(nc_file)

# 3. View latitude and longitude values
lat_lst = nc_file["__xarray_dataarray_variable__"]["latitude"].values[:]
lon_lst = nc_file["__xarray_dataarray_variable__"]["longitude"].values[:]
#print('latitude',lat_lst)
#print('longitude',lon_lst)

# 4. View xarray values in netCDF file
value = np.flip(nc_file['__xarray_dataarray_variable__'].T)

# 5. Set Raster data property 
value = value.rio.set_spatial_dims('longitude','latitude')
value.rio.crs
value.rio.set_crs("epsg:4326")

# 6. Convert from netCDF to GeoTiff, and output GeoTiff file 
value.rio.to_raster(r"to_raster.tiff")