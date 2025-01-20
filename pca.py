import copy
import numpy as np
from matplotlib import pyplot as plt
import math
import chamferdistance as cdis
import wrtxt
import wrtxt as wt
from rpca import robust_pca

true_list = []
precision = 0
R_list = np.load("road.npy", allow_pickle=True)
P_list = np.load("park.npy", allow_pickle=True)
best_park_list = np.load("true.npy", allow_pickle=True)
num = 0
long_len = 0
for index in range(51):
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
    # a = np.random.random((len_P, 1)) / 5000  # 0.0002 and  0.0005
    # b = np.random.random((len_P, 1)) / 5000
    b = np.zeros((len_P, 1))
    # c = np.c_[a, b]
    # P = P + a
    long_len += len_P
    # P = initial(P)  # 输入的偏移park
    # R = initial(R)
    # P = tftmatrox(P, math.pi * -15 / 180, [0, 0])
    # P = P + [0.0020, -0.0001]
    # len_R = len(R)
    # len_P = len(P)
    min_los = 999999
    beststart = 2
    for startpoint in range(len_R - len_P + 1):
        R_ = R[startpoint:startpoint + len_P]
        R_ = R_.reshape(2*len_P,1)
        P = P.reshape(2*len_P,1)
        data = np.c_[P,R_]
        loss2,loss = robust_pca(data)
        loss = np.sum(loss)
        if loss < min_los:
            min_los = loss
            beststart = startpoint
    # plt.scatter(R[:, 0], R[:, 1], label="predicted parking spaces", c="r")
    best_park_GPS = R[beststart:beststart + len_P]
    if len(best_park_GPS) == len(best_park):
        for item in range(len(best_park)):
            if best_park_GPS[item] in best_park:
                num += 1
        a = np.mean(np.abs(best_park_GPS - best_park))
    else:
        print(index)
        break
    precision += a
    print(index)
num_av = num / long_len
num_per = num / 51
precision = precision / 51
print('定位偏差', precision)
print("召回率：", num_av)