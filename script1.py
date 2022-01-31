from netCDF4 import Dataset, num2date
import time
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import pandas as pd

data_types = ['lrad', 'prec', 'pres', 'shum', 'srad', 'temp', 'wind']
data_type = data_types[-1]
# data_type = 'temp'

file_temp = r'/Volumes/mac_data/andy/气象数据1979-2018/Data_forcing_01mo_010deg/{}_CMFD_V0106_B-01_01mo_010deg_197901-201812.nc'
nc = Dataset(file_temp.format(data_type))
# nc = Dataset(r'/Volumes/mac_data/andy/气象数据1979-2018/Data_forcing_01yr_010deg/{}_CMFD_V0106_B-01_01yr_010deg_1979-2018.nc'.format(data_type))

time_data = nc.variables['time'][:]
dtime = num2date(time_data, nc.variables['time'].units)

lon_data = nc.variables['lon'][:]
# lon_data_filtered = np.ma.where((lon_data > 108.6579464814453) & (lon_data < 108.96968354199217), lon_data, 0)
# lon_data.mask = True
# lon_data[(lon_data >= 108.6579464814453) & (lon_data <= 108.96968354199217)] = ma.nomask
lon_data_index = ma.where((lon_data >= 108.691418) & (lon_data <= 108.96968354199217))[0]

lat_data = nc.variables['lat'][:]
lat_data_index = ma.where((lat_data >= 40.772188) & (lat_data <= 41.132830))[0]
# lat_data.mask = True
# lat_data[(lat_data >= 40.76280589461345) & (lat_data <= 41.15378744480841)] = ma.nomask

target_data = nc.variables[data_type][:]

for i, dtime_year in enumerate(dtime[-12 * 5:]): # 最近xxx 条数据

    print('start to plot', dtime_year)
    time.sleep(1)

    test = np.zeros((len(lat_data_index), len(lon_data_index)))

    for j, lat_index_j in enumerate(lat_data_index):
        for k, lon_index_k in enumerate(lon_data_index):
            test[j,k] = target_data[i][lat_index_j, lon_index_k]


    # print(test)
    plt.contourf(lon_data[lon_data_index], lat_data[lat_data_index], test)
    # plt.contourf(lon_data_filtered, lat_data_filtered, test)
    plt.colorbar()
    plt.title('{}_{}'.format(data_type, dtime_year))
    plt.show()
