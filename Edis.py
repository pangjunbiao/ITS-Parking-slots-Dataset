import numpy as np
from matplotlib import pyplot as plt
import wrtxt
import gps_distance_google

def distence(xu, yu):
    distence_sum = 0
    for i in range(np.size(xu)):
        distence_temp = xu[i] - yu[i]
        distence_sum += distence_temp ** 2
    return distence_sum

def getsite (xu,yu):
    #寻找最小的err的起点
    site = 0
    temp = 500000
    for i in range(0,np.size(yu)-np.size(xu),2):
        n = np.size(xu)
        R_new = yu[i:n+i]
        Err = distence(xu,R_new)
        if Err < temp:
            temp = Err
            site = i
    return site,temp


R = np.load("R_test.npy", allow_pickle=True)
P = np.load("P_test.npy", allow_pickle=True)
len_P = len(P)
len_R = len(R)
P = P.reshape(2 * len_P, 1)
R = R.reshape(2 * len_R, 1)
best_site, err = getsite(P, R)
R = R.reshape(len_R, 2)
P = P.reshape(len_P, 2)
best_park_GPS = R[int(best_site / 2):int(best_site / 2 + len_P), ].copy()
# plt.scatter(P[:, 0], P[:, 1], label="collected　parking　spaces", c="b")
# plt.scatter(best_park_GPS[:, 0], best_park_GPS[:, 1], c="k", label="matched parking spaces")
# # plt.ylim(-0.0015,0.007)
# # plt.xlim(-0.0015,0.007)
# plt.legend(fontsize=20)
# plt.show()
# wrtxt.writetxtred(R, "ed.mif")
# wrtxt.writetxtblue(P, "ed.mif")
# wrtxt.writetxtblack(best_park_GPS, "ed.mif")

#数据集性能
best_park_GPS = best_park_GPS.reshape(len_P, 2)
R_list =np.load("Road.npy",allow_pickle=True)
P_list = np.load("Park.npy",allow_pickle=True)
best_park_list = np.load('gt.npy',allow_pickle=True)
curse_list = [0, 4, 9, 12, 13, 17, 21, 22, 25, 27, 28]
num=0
precision = 0
long_len = 0
n=0
for index in range(len(P_list)):
# for index in curse_list:
    if index in curse_list:
        continue
    n+=1

    P = P_list[index]
    R = R_list[index]
    best_park = best_park_list[index]
    len_P = len(P)
    len_R = len(R)
# 引入的随机干扰
    # np.random.seed(999)
    # a = np.random.random((len_P, 1)) / 3000  # 0.0002 and  0.0005
    # b = np.random.random((len_P, 1)) / 3000
    # b = np.zeros((len_P, 1))
    # c = np.c_[a, b]
    # P = P + a
    P = P.reshape(2 * len_P, 1)
    R = R.reshape(2 * len_R, 1)
    best_site, err = getsite(P, R)
    R = R.reshape(len_R, 2)
    P = P.reshape(len_P, 2)
    best_park_GPS = R[int(best_site / 2):int(best_site / 2 + len_P), ].copy()
    best_park_GPS = best_park_GPS.reshape(len_P, 2)
    long_len +=len_P
    # plt.scatter(P[:, 0], P[:, 1], label="collected　parking　spaces", c="b")
    # plt.scatter(best_park[:, 0], best_park[:, 1], c="k", label="matched parking spaces")
    # plt.ylim(-0.0015,0.007)
    # plt.xlim(-0.0015,0.007)
    # plt.legend(fontsize=20)
    # plt.show()
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
num_per = num / n
precision = gps_distance_google.do(precision / n)
print('定位准确度', precision)
print("准确数目：", num, "准确率：", num_av)