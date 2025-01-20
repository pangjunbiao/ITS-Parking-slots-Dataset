import numpy as np
import readlist
import matplotlib.pyplot as plt
import strfloat

def readtxt():
    f = open(r"way4.txt")
    file = f.read()
    gps_lng_dict = {}
    gps_lat_dict = {}

    line = file.split('\n')

    cols_name,start_cols_lon,start_cols_lat,last_cols_lon,last_cols_lat = readlist.read_excel()
    for temp in line :
        lat = []
        lng = []
        # if cols_name[index_num] != "翠屏南里街（南侧）":
        #     index_num = index_num + 1
        #     continue
        index_num = int(temp.split('/')[0])
        point_gps = temp.split('/')[1].split(',')
        gps_lng_dict[cols_name[index_num]] = []
        gps_lat_dict[cols_name[index_num]] = []

        for i in range(np.size(point_gps)):
            if point_gps[i] == '':
                continue
            if (i%2 == 0):
                gps_lng_dict[cols_name[index_num]].append(point_gps[i])
            if ((i%2)==1):
                gps_lat_dict[cols_name[index_num]].append(point_gps[i])
        # if (np.size(gps_lng_dict[cols_name[index_num]]+np.size(gps_lat_dict[cols_name[index_num]])%2 == 1):
        #     gps_lng_dict[cols_name[index_num]] = []
        #     gps_lat_dict[cols_name[index_num]] = []
        #     point_gps = temp.split(',')[3:-1]
        #     for i in range(np.size(point_gps)):
        #         if point_gps[i] == '':
        #             continue
        #         if (i % 2 == 0):
        #             gps_lng_dict[cols_name[index_num]].append(point_gps[i])
        #         if ((i % 2) == 1):
        #             gps_lat_dict[cols_name[index_num]].append(point_gps[i])
        # gps_lng_dict[cols_name[index_num]] = lng
        # gps_lat_dict[cols_name[index_num]] = lat
        index_num=index_num+1
    # f.close()
    return gps_lat_dict,gps_lng_dict

if __name__ == '__main__':
    lat,lng = readtxt()
    cols_name,start_cols_lon,start_cols_lat,last_cols_lon,last_cols_lat = readlist.read_excel()
    # plt.scatter(lng["新街口外大街西"],lat["新街口外大街西"])
    temp_lon, temp_lat = strfloat.transform(lng["翠屏南里街（南侧）"], lat["翠屏南里街（南侧）"])
    plt.scatter(temp_lon, temp_lat)
    plt.scatter(last_cols_lon[1000], last_cols_lat[1000])
    plt.scatter(start_cols_lon[1000], start_cols_lat[1000])
    plt.show()
    # print(lat["南新华街（东侧）"])
    # print(lng["南新华街（东侧）"])

