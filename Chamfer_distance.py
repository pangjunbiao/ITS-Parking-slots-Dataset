import copy

import numpy as np
from matplotlib import pyplot as plt
import math
import chamferdistance as cdis
import wrtxt
import wrtxt as wt
#倒角距离
def initial(x):
    lon = copy.copy(x[:,0])
    lat = copy.copy(x[:,1])
    min_lon = np.min(lon)
    min_lat = np.min(lat)
    lon = lon-min_lon
    lat = lat-min_lat
    lon_lat = np.c_[lon,lat]
    return lon_lat


def tft(theta, Ou=np.array([0, 0])):
    # theta1*1，O为2*2
    # 生成旋转矩阵

    mateix = np.array([[math.cos(theta), -math.sin(theta),
                        (1 - math.cos(theta)) * float(Ou[0]) + float(Ou[1]) * (math.sin(theta))],
                       [math.sin(theta), math.cos(theta),
                        (1 - math.cos(theta)) * float(Ou[0]) - float(Ou[1]) * (math.sin(theta))],
                       [0, 0, 1]])

    return mateix


def tftmatrox(P, theta, Ou):
    # 对坐标点进行旋转
    # 输入n*2输出n*2
    tft_matrix = tft(theta, Ou)
    b = []
    for temp in P:
        ex_temp = np.array([temp[0], temp[1], 1]).T
        tft_point = np.dot(tft_matrix, ex_temp)
        b.append(tft_point)
    b = np.array(b)
    return b[:, 0:2]


if __name__ =='__main__':
    # R = np.array([[116.36451199999962, 39.86813945454547, ],
    #           [116.36466399999924, 39.86813254545458, ],
    #           [116.36481599999885, 39.868125636363686, ],
    #           [116.36496799999847, 39.868118727272794, ],
    #           [116.36511999999809, 39.86811181818191, ],
    #           [116.3652719999977, 39.86812039999954, ],
    #           [116.36542499999732, 39.86812275862088, ],
    #           [116.36557699999693, 39.86811227586228, ],
    #           [116.36572999999655, 39.86811727272706, ],
    #           [116.36588199999616, 39.868126484848254, ],
    #           [116.36603499999578, 39.86812512820534, ],
    #           [116.36618699999539, 39.86811733333357, ],
    #           [116.36633899999501, 39.86811, ],
    #           [116.36649199999462, 39.86811, ],
    #           [116.36664499999424, 39.868113166666475, ],
    #           [116.36679799999385, 39.86811826666646, ],
    #           [116.36695099999346, 39.86812309090869, ],
    #           [116.36710299999308, 39.86813230302988, ],
    #           [116.3672549999927, 39.86814, ],
    #           [116.36740799999231, 39.86814, ],
    #           [116.36756099999192, 39.86814, ],
    #           [116.36771399999154, 39.86814335483844, ],
    #           [116.36786699999115, 39.868148290322296, ],
    #           [116.36801899999077, 39.868155436572806, ],
    #           [116.36817099999038, 39.868163783634834, ],
    #           [116.36832299999, 39.86817170250066, ],
    #           [116.36847499998962, 39.868178372092565, ],
    #           [116.36862699998923, 39.86818504168448, ],
    #           [116.36877899998885, 39.86819149999957, ],
    #           [116.36893099998846, 39.8681973461534, ],
    #           [116.36908399998808, 39.8682, ],
    #           [116.36923699998769, 39.8682, ],
    #           [116.3693899999873, 39.86820166666614, ],
    #           [116.36954199998692, 39.868207999999456, ],
    #           [116.36969399998654, 39.86820013793057, ],
    #           [116.36984699998615, 39.86820541379262, ],
    #           [116.36999899998577, 39.86821071698059, ],
    #           [116.37015099998538, 39.868216452829635, ],
    #           [116.370302999985, 39.86822218867868, ],
    #           [116.37045499998462, 39.868227924527716, ],
    #           [116.37060699998423, 39.868233592592006, ],
    #           [116.37075899998385, 39.868239222221625, ],
    #           [116.37091099998347, 39.868244851851244, ],
    #           [116.37106399998308, 39.86825, ],
    #           [116.3712129999827, 39.86822562501081, ],
    #           [116.37127399998255, 39.8681160001483, ],
    #           [116.37128799998251, 39.86799700014861, ],
    #           [116.37130199998248, 39.86787800014892, ],
    #           [116.37131599998244, 39.867759000149235, ],
    #           [116.37132999998241, 39.86764000014954, ],
    #           [116.37134399998237, 39.867521886815375, ],
    #           [116.37135799998234, 39.867403773482316, ],
    #           ])
    # P = np.array([[116.36908399998808, 39.8682, ],
    #           [116.36923899998769, 39.86822, ],
    #           [116.3693899999873, 39.86823166666614, ],
    #           [116.36954199998692, 39.868457999999456, ],
    #           [116.36968399998654, 39.86834013793057, ],
    #           [116.36985699998615, 39.86820541379262, ],
    #           [116.36999899998577, 39.86821071698059, ],
    #           [116.37015099998538, 39.868216452829635, ],
    #           [116.370302999985, 39.86822218867868, ],
    #           [116.37045499998462, 39.868227924527716, ],
    #           [116.37060699998423, 39.868243592592006, ],
    #           [116.37075899998385, 39.868239222221625, ],
    #           [116.37091199998347, 39.868244851851244, ],
    #           [116.37106359998308, 39.86865, ],
    #           [116.3712122999827, 39.86852562501081, ],
    #           [116.37127399998255, 39.8681160001483, ],
    #           [116.37128799998251, 39.86799700014861, ],
    #           [116.371301129998248, 39.86757800014892, ],
    #           [116.37131599998244, 39.867759000149235, ],
    #           [116.37133599998241, 39.86764000014954, ],
    #           [116.371343899998237, 39.867521886815375, ],
    #           [116.37133789998234, 39.867403773482316, ],
    #           ])
    # lon = copy.copy(R[:, 0])
    # lat = copy.copy(R[:, 1])
    # min_lon = np.min(lon)
    # min_lat = np.min(lat)
    # P = initial(P)  # 输入的偏移park
    # R = initial(R)
    # P = tftmatrox(P, math.pi * -15 / 180, [0, 0])
    # P = P + [0.0020, -0.0005]
    # len_R = len(R)
    # len_P = len(P)
    # P += [min_lon,min_lat]
    # R += [min_lon,min_lat]
    # np.save("R_test", R, allow_pickle=True)
    # np.save("P_test", P, allow_pickle=True)
    # min_los = 999999
    # beststart = 2
    # for startpoint in range(len_R - len_P + 1):
    #     R_ = R[startpoint:startpoint + len_P]
    #     loss = cdis.chamferdistance(R_, P)
    #     if loss < min_los:
    #         min_los = loss
    #         beststart = startpoint
    # plt.scatter(R[:, 0], R[:, 1], label="predicted parking spaces", c="r")
    # best_park_GPS = R[beststart:beststart + len_P]
    # plt.scatter(P[:, 0], P[:, 1], label="collected　parking　spaces", c="b")
    # plt.scatter(best_park_GPS[:, 0], best_park_GPS[:, 1], c="k", label="matched parking spaces")
    # plt.show()
    # wrtxt.writetxtblack(best_park_GPS,"cd.mif")
    # wrtxt.writetxtred(R,"cd.mif")
    # wrtxt.writetxtblue(P,"cd.mif")

    #对数据集
    true_list = []
    curse_list = [0,4,9,12,13,17,21,22,25,27,28]
    precision =  0
    R_list = np.load("road.npy",allow_pickle=True)
    P_list = np.load("park.npy",allow_pickle=True)
    best_park_list = np.load("gt.npy",allow_pickle=True)
    num = 0
    long_len = 0
    np.random.seed(999)
    # for index in range(51):
    for index in curse_list:
        # if index in curse_list:
        #     continue
        # index =5
        R = R_list[index]
        P = P_list[index]
        best_park = best_park_list[index]
        P_old = copy.copy(P)
        lon = copy.copy(R[:, 0])
        lat = copy.copy(R[:, 1])
        min_lon = np.min(lon)
        min_lat = np.min(lat)
        len_P = len(P)
        len_R = len(R)
        a = np.random.random((len_P,1))/5000      #0.0002 and  0.0005
        b = np.random.random((len_P,1))/5000
        b = np.zeros((len_P,1))
        c = np.c_[a,b]
        P = P+a
        long_len += len_P
        # P = initial(P)  # 输入的偏移park
        # R = initial(R)
        # P = tftmatrox(P, math.pi * -15 / 180, [0, 0])
        # P = P + [0.0020, -0.0001]
        # len_R = len(R)
        # len_P = len(P)
        min_los = 999999
        beststart = 2
        for startpoint in range(len_R-len_P+1):
            R_ = R[startpoint:startpoint+len_P]
            loss = cdis.chamferdistance(R_,P)
            if loss<min_los:
                min_los=loss
                beststart = startpoint
        # plt.scatter(R[:, 0], R[:, 1], label="predicted parking spaces", c="r")
        # plt.ylim(min_lat-0.0015,min_lat+0.003)
        # plt.xlim(min_lon-0.0006,min_lon+0.007)
        # plt.show()
        best_park_GPS = R[beststart:beststart + len_P]
        if len(best_park_GPS)==len(best_park):
            for item in range(len(best_park)):
                if best_park_GPS[item] in best_park:
                    num += 1
            a = np.mean(np.abs(best_park_GPS - best_park))
        else:
            print(index)
            break
        precision += a
        print(index)
    #print("道路平均停车位数目：",long_len/51) # 直线
    print("道路平均停车位数目：", long_len / 11)  # 曲线
    num_av = num/long_len
    #num_per = num/51 # 直线
    num_per = num / 11  # 曲线
    precision = precision / 11
    print('定位偏差',precision)
    print("召回率：",num_av)

