# -*-encoding:utf-8-*-
import csv
import math
import matplotlib.pyplot as plt
import numpy as np

def check_onlyway(data_direction):
    for link_id in data_direction :
        number_same = 0
        for temp_id in data_direction:
            if link_id == temp_id:
                number_same += 1
            if number_same >= 2:
                return True
    return False

def check_two_way(data):
    split_list = []
    j = data[0]
    for a in range(np.shape(data)[0]):
        i = data[a]
        err = (j[0] - i[0] + j[1] - i[1])
        if  abs(err) > 0.2:
            split_list.append(a)
        j = data[a]
    if split_list == []:
        return False
    else:
        return True
def get_twoway_point(data):
    split_list = []
    j = data[0]
    for a in range(np.shape(data)[0]):
        i = data[a]
        err = (j[0] - i[0] + j[1] - i[1])
        if  abs(err) > 0.2:
            split_list.append(a)
        j = data[a]
    return split_list
def transform(list_str):
    #将字符串转化为浮点型
    list_float=[]
    for index in list_str:
        if index == 'null':
            continue
        index = float(index)
        # print(type(index))
        list_float.append(index)
    return list_float

def getoutintrupt(line):
    #去除读取的数据中的干扰字符
    good= ""
    for i in line:
        if i == '[':
            continue
        if i == ']':
            continue
        if i == '}':
            continue
        good += i
    good = good.split(',')
    return good

def getoutintrup_array(line):
    #去除读取的数据中的干扰字符输出更便于输出数组形式的list
    link_gps = []
    good = ""
    for i in line:
        if i == '[':
            good = ""
            continue
        if i == ']':
            link_gps.append(transform(good.split(',')))
            continue
        if i == '}':
            continue
        good += i
    return link_gps

def getlkrange(link_gps):
    #获取link的范围
    max_lat = 0
    min_lat = 100
    max_lon = 0
    min_lon = 200
    for i in link_gps:
        if i < 100:
            if i > max_lat:
                max_lat = i
            if i < min_lat:
                min_lat = i
        else :
            if i > max_lon:
                max_lon = i
            if i < min_lon:
                min_lon = i
    link_range =np.array([[min_lon,min_lat],[max_lon,max_lat]])
    return link_range
# class Gps:
#     def __init__(self,gps,name,link_id,direction):
#         self.gps = gps
#         self.name = name
#         self.link_id = link_id
#         self.direction = direction
def read():
    #阅读CSV文件。返回gps_lon为道路GPS的经度坐标，gps_lat为道路GPS的纬度坐标。
    csv_file=csv.reader(open('roadRticLink_21q2_20210630.csv','r',errors='ignore',encoding='utf-8'))
    road_gps = {}#key值为道路名称，value为道路经纬度坐标
    link_range = {} #link中包含的gps点的最大最小值
    name_link = {} #name中包含的linkid
    road_direction = {} #道路的方向
    link_type = {} #储存link的类型
    link_dict = {}
    name_dir_link = {}
    number = 0
    for line in csv_file:
        number += 1
        line_con = ""
        for index in range(len(line)):
            line_con = line_con+','+line[index]
        line_point = line_con.split(";")
        # print(len(line_point))
        if number == 1:
            continue
        line_name = line_point[1]
        line_direction = line_point[3]
        link_id = line_point[-4]
        line_type = line_point[-2][-1]
        link_gps_str = line_point[-1].split(':')[-1]
        link_gps = getoutintrup_array(link_gps_str) #可直接转化为数组的列表
        simp_link_gps = transform(getoutintrupt(link_gps_str)) #只包含坐标没有成对的列表
        line_name_dir = line_name+line_direction
        if line_name_dir not in road_gps.keys():
            road_gps[line_name_dir] = []
        road_gps[line_name_dir].extend(link_gps)
        if link_id not in link_range.keys():
            link_range[link_id] = []
        link_range[link_id] = getlkrange(simp_link_gps)
        if line_name not in road_direction.keys():
            road_direction[line_name] = []
        if int(line_direction) not in road_direction[line_name]:
            road_direction[line_name].append(int(line_direction))
        if line_name not in name_link.keys():
            name_link[line_name] = []
        name_link[line_name].append(link_id)
        #判断道路类型
        if line_name_dir not in link_type.keys():
            link_type[line_name_dir] = []
        link_type[line_name_dir].extend(line_type)
        if link_id not in link_dict:
            link_dict[link_id] = []
        link_dict[link_id] = link_gps
        if line_name_dir not in name_dir_link.keys():
            name_dir_link[line_name_dir] = []
        name_dir_link[line_name_dir].append(link_id)
        #辅路代替主路
    for temp_name in road_gps.keys():
        if temp_name[-2] =='辅' and temp_name[-1] == '路':
            road_gps[temp_name[:-2]] = road_gps[temp_name]
    return road_gps,link_range,road_direction,name_link,link_type,link_dict,name_dir_link


if __name__ == '__main__':
    road_gps,link_range,road_direction,name_link,link_type,link_dict,name_dir_link = read()
    # print(road_direction['西直门南小街'])#方向——list
    print(name_dir_link["西直门南小街5"])
    # # list_temp = name_link["西直门南小街"]
    print(link_type["西直门南小街5"])
    # print(link_dict['63025413'])

    # print(name_link["春和路"])#link_list
    # #可视化
    n = 0
    # for i in name_dir_link['崇文门外大街1']:
    #     n+=1
    #     if n <20:
    #         continue
    #     plt.plot(np.array(link_dict[i])[:,0],np.array(link_dict[i])[:,1])
    #     n+=1
        # if n == 10:
        #     break
    # plt.show()
    # plt.scatter(np.array(link_dict["'63025413'"])[:,0],np.array(road_gps["定慧东街1"])[:,1],)
    # plt.scatter(np.array(road_gps["定慧东街5"])[:,0],np.array(road_gps["定慧东街5"])[:,1],)
    # plt.scatter(np.array(road_gps["朝阳北路3"])[:,0],np.array(road_gps["朝阳北路3"])[:,1],)
    # plt.scatter(np.array(road_gps["朝阳北路7"])[:,0],np.array(road_gps["朝阳北路7"])[:,1],)

    # plt.show()
    # for index in road_gps.keys():
    #     if len(road_direction[index[:-1]]) <= 2:
    #         temp = np.array(road_gps[index])
    #         plt.scatter(temp[:,0],temp[:,1])
    #         print(index)
    #         plt.show()

    # print(check_two_way(np.array(road_gps["北大街3"])))
    # if check_two_way(np.array(road_gps["北大街3"])):
    #     lon_lat_1 = np.array(road_gps["北大街3"])[:164]
    #     lon_lat_2 = np.array(road_gps["北大街3"])[164:]



    # for i in name_link["春和路"]:
    #     print(link_range[i])
    # plt.scatter(lon_lat_1[:,0],lon_lat_1[:,1])
    # plt.scatter(lon_lat_2[:,0],lon_lat_2[:,1])
    # print()
    # plt.scatter(np.array(road_gps["东四块玉南街1"])[:,0],np.array(road_gps["东四块玉南街1"])[:,1],color='red')
    # plt.scatter(np.array(road_gps["东四块玉南街5"])[:,0],np.array(road_gps["东四块玉南街5"])[:,1],color='blue')
    # print(name_link["东四块玉南街"])
    # print(check_onlyway(name_link['东四块玉南街']))
    #
    # if road_gps["厂西门南路3"] == road_gps["厂西门南路7"]:
    #     print("一样")

    # # plt.scatter(np.array(road_gps["参政西巷1"])[:,0],np.array(road_gps["参政西巷1"])[:,1])

    # plt.scatter(np.array(road_gps["朝阳北路2"])[:,0],np.array(road_gps["朝阳北路2"])[:,1],)
    # plt.scatter(np.array(road_gps["朝阳北路6"])[:,0],np.array(road_gps["朝阳北路6"])[:,1],)
    # plt.scatter(np.array(road_gps["朝阳北路4"])[:,0],np.array(road_gps["朝阳北路4"])[:,1],)
    # plt.scatter(np.array(road_gps["朝阳北路3"])[:,0],np.array(road_gps["朝阳北路3"])[:,1],)
    # plt.scatter(np.array(road_gps["朝阳北路7"])[:,0],np.array(road_gps["朝阳北路7"])[:,1],)
    plt.show()





