from scipy.interpolate import interp1d
import numpy as np
import copy
import matplotlib.pyplot as plt

def interk(lon,lat):
    # lon_lat_list =[]
    lat_train = copy.copy(lat)
    lon_train = copy.copy(lon)
    max_lon = max(lon)
    min_lon = min(lon)
    max_lat = max(lat)
    min_lat = min(lat)
    err_lat = max_lat - min_lat
    err_lon = max_lon-min_lon
    if err_lat >= err_lon:
        # lon_lat = np.c_[lat_train, lon_train]
        # numsort = np.argsort(lon_lat[:, 0], axis=0)
        # for tempnum in numsort:
        #     lon_lat_list.append(lon_lat[tempnum])
        # lon_lat_arr = np.array(lon_lat_list)
        # x = lon_lat_arr[:, 1]
        # y = lon_lat_arr[:, 0]
        x = lat_train
        y = lon_train
        f = interp1d(x, y)
        x_1 = min(lat_train)
        y_1 = max(lat_train)
        test_x = np.arange(x_1, y_1, 0.000001)
        test_y = f(test_x)
        lat_test_ = test_x
        lon_test_ = test_y
    if err_lat < err_lon:
        # lon_lat = np.c_[lon_train,lat_train]
        # numsort = np.argsort(lon_lat[:, 0], axis=0)
        # for tempnum in numsort:
        #     lon_lat_list.append(lon_lat[tempnum])
        # lon_lat_arr = np.array(lon_lat_list)
        # x = lon_lat_arr[:, 1]
        # y = lon_lat_arr[:, 0]
        x = lon_train
        y = lat_train
        f = interp1d(x, y)
        x_1 = min(x)
        y_1 = max(x)
        test_x = np.arange(x_1, y_1, 0.000001)
        test_y = f(test_x)
        lat_test_ = test_y
        lon_test_ = test_x
        # plt.plot(lat_test_,lat_test_)
    return  lon_test_,lat_test_,


