from netCDF4 import Dataset, num2date
import time
import numpy as np
import numpy.ma as ma
from collections import defaultdict
from Util.CSVHelper import export_dict_rows_to_csv


data_types = ['lrad', 'prec', 'pres', 'shum', 'srad', 'temp', 'wind']
data_type = data_types[-1]
# lake_name = '乌梁素海'
# lake_name = '呼伦湖'
# lake_name = '达里湖'
# lake_name = '红碱淖'
lake_name = '岱海'

file_temp = r'/Volumes/mac_data/andy/气象数据1979-2018/Data_forcing_01mo_010deg/{}_CMFD_V0106_B-01_01mo_010deg_197901-201812.nc'
nc = Dataset(file_temp.format(data_type))
# nc = Dataset(r'/Volumes/mac_data/andy/气象数据1979-2018/Data_forcing_01yr_010deg/{}_CMFD_V0106_B-01_01yr_010deg_1979-2018.nc'.format(data_type))

time_data = nc.variables['time'][:]
dtime = num2date(time_data, nc.variables['time'].units)

lon_data = nc.variables['lon'][:]
lat_data = nc.variables['lat'][:]
all_data = nc.variables[data_type][:]

def get_lon_lat_data_index_target_points():
    left_corner = ()
    right_corner = ()
    if lake_name == '乌梁素海':
        left_corner = (40.74, 108.641418)
        right_corner = (41.16, 109.06968354199217)
    elif lake_name == '呼伦湖':
        left_corner = (48.52333619858433, 116.91069673381983)
        right_corner = (49.38988270208055, 117.86788050669196)
    elif lake_name == '达里湖':
        left_corner = (43.212944264941626, 116.47484757435343)
        right_corner = (43.45182011950481, 116.75569748918798)
    elif lake_name == '红碱淖':
        left_corner = (39.049003357702595, 109.79469995082037)
        right_corner = (39.1577283801992, 109.95941216010742)
    elif lake_name == '岱海':
        left_corner = (40.52004586375066, 112.58529622799206)
        right_corner = (40.633739443761364, 112.79781299822443)

    lon_data_index = ma.where((lon_data >= left_corner[1]) & (lon_data <= right_corner[1]))[0]
    print(list(lon_data[(lon_data >= left_corner[1]) & (lon_data <= right_corner[1])]))
    lat_data_index = ma.where((lat_data >= left_corner[0]) & (lat_data <= right_corner[0]))[0]
    print(list(lat_data[(lat_data >= left_corner[0]) & (lat_data <= right_corner[0])]))
    return lon_data_index, lat_data_index


def get_target_points():
    target_points = []
    if lake_name == '乌梁素海':
        target_points = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3)]
    elif lake_name == '呼伦湖':
        target_points = [(0,2), (0,3), (1,2), (1,3), (1,4), (2,0), (2,1), (2,2), (2,3), (2,4), (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (6,3), (6,4), (6,5), (6,6), (6,7), (7,4), (7,5), (7,6), (7,7), (8,5), (8,6), (9,6)]
    elif lake_name == '达里湖':
        target_points = [(0,0), (1,0), (1,1), (2,0)]
    elif lake_name == '红碱淖':
        target_points = [(0,0), (0,1), (1,0), (1,1)]
    elif lake_name == '岱海':
        target_points = [(0,0), (0,1)]
    return target_points


target_data = defaultdict(list)
target_points = get_target_points()
lon_data_index, lat_data_index = get_lon_lat_data_index_target_points()

for i, dtime_year in enumerate(dtime[:]): # 最近xxx 条数据
    for j, lon_index_j in enumerate(lon_data_index):
        for k, lat_index_k in enumerate(lat_data_index):
            if (j,k) in target_points:
                value = all_data[i][lat_index_k, lon_index_j]
                target_data[str(dtime_year)].append(value)


export_data = []


for key, val in target_data.items():
    export_data.append({'date': key, 'mean': np.mean(val)})

export_dict_rows_to_csv('{}_wind_mean.csv'.format(lake_name), export_data, export_data[0].keys())
