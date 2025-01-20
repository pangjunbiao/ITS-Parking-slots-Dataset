# -*-encoding:utf-8-*-
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
def read():
    #阅读CSV文件。返回gps_lon为道路GPS的经度坐标，gps_lat为道路GPS的纬度坐标。
    csv_file=csv.reader(open('road_19Q3_2019.csv','r',errors='ignore',encoding='utf-8'))
# print(csv_file) #可以先输出看一下该文件是什么样的类型
    gps_lon={}#key值为道路名称，value为道路经度坐标
    gps_lat={}#key值为道路名称，value为道路纬度坐标
    for line in csv_file:
        line_con = ""
        for index in range(len(line)):
            line_con = line_con+','+line[index]
        line_point = line_con.split("\x01")
        line_point_col = line_point[-3]
        null = 'null'
        if line_point_col == null:
            continue
        name_point = line_point[-3].split(",")[1]
        gps_point = line_point[-2].split(";")
        link_size = len(gps_point)

        if name_point not in gps_lon.keys():
            gps_lon[name_point]=[]
        if name_point not in gps_lat.keys():
            gps_lat[name_point] = []
        for index in range(link_size):
            gps_point_lon = gps_point[index].split(",")[0]
            gps_point_lat = gps_point[index].split(",")[1]
            gps_lon[name_point].append(gps_point_lon)
            gps_lat[name_point].append(gps_point_lat)
    return gps_lat,gps_lon

if __name__ == '__main__':
    lat,lon = read()
    lat_nan=[]
    lon_nan=[]
    for index in lat['开阳里一街']:
        index = float(index)
        lat_nan.append(index)
    for index in lon['开阳里一街']:
        index=float(index)
        lon_nan.append(index)
    lat_nan=np.array((lat_nan))
    print(lat_nan)
    lon_nan=np.array((lon_nan))
    print(lon_nan)
    # print(np.size(lat_nan))
    # print(np.size(lon_nan))
    plt.scatter(lon_nan,lat_nan)#绘制道路GPS点
    plt.ylim(39.8,40)
    plt.show()
