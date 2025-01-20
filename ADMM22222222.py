# 导入sympy包，用于求导，方程组求解等等
from sympy import *
import copy
import numpy as np
import math
# import tftmatrox
from S_t import softmax
from tftmatrox import transform
from shape import fsvd
import matplotlib.pyplot as plt
import wrtxt as wt
import gps_distance_google

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

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
def setR(x, y):
    # 输入n*2，输出2n*1
    min1 = min(np.min(x[:, 0]), np.min(y[:, 0]))
    min2 = min(np.min(x[:, 1]), np.min(y[:, 1]))
    a = np.c_[(y[:, 0] - min1), y[:, 1] - min2]
    # a = a.reshape((len_P*2,1))
    return a

def setP(x, y):
    # 输入n*2，输出2n*1
    min1 = min(np.min(x[:, 0]), np.min(y[:, 0]))
    min2 = min(np.min(x[:, 1]), np.min(y[:, 1]))
    a = np.c_[(x[:, 0] - min1), x[:, 1] - min2]
    # a = a.reshape((len_P*2,1))
    return a


def admm(P_, R_):
    # 输入P为停车点的gps数组，大小为n*2，R为路链的GPS大小为m*2（m>n）
    # L=||E_1||+lamuda||A||_(r=1)+<Y_1,theta_0.P+delta tehta(theta-tehta_0))略
    def maxminnorn(x):
        list_1 = []
        list_2 = []
        lon = x[:, 0]
        lat = x[:, 1]
        max_lat = np.max(lat)
        min_lat = np.min(lat)
        max_lon = np.max(lon)
        min_lon = np.min(lon)
        for i in lon:
            t = (i - (min_lon)) / (max_lon - min_lon)
            list_1.append(t)
        for i in lat:
            k = (i - (min_lat)) / (max_lat - min_lat)
            list_2.append(k)
        list_1 = np.array(list_1)
        list_2 = np.array(list_2)
        resort = np.c_[list_1, list_2]
        return resort

    def getOu(X):
        lt = copy.copy(X[:, 1])
        lt.sort()
        ln = copy.copy(X[:, 0])
        ln.sort()
        lt_range = lt[-1] - lt[0]
        ln_range = ln[-1] - ln[0]
        if ln_range >= lt_range:
            h = min(X[:, 0])
            w = np.where(X[:, 0] == h)
            w = np.array(w)
            # if np.size(w) > 1:
            w = int(w[0][0])
            Ou = X[w]
        if ln_range < lt_range:
            h = min(X[:, 1])
            w = np.where(X[:, 1] == h)
            w = np.array(w)
            # if len(w) > 1:
            w = int(w[0][0])
            Ou = X[w]
        # r = float(Ou[:,0])
        return Ou

    def tft(theta, Ou = np.array([0, 0])):
        # theta1*1，O为2*2
        # 生成旋转矩阵

        mateix = np.array([[math.cos(theta), -math.sin(theta),
                            (1 - math.cos(theta)) * float(Ou[ 0]) + float(Ou[1]) * (math.sin(theta))],
                           [math.sin(theta), math.cos(theta),
                            (1 - math.cos(theta)) * float(Ou[ 0]) - float(Ou[1]) * (math.sin(theta))],
                           [0, 0, 1]])

        return mateix

    def jacobi(theta, P, Ou=np.array([0, 0])):
        # tehta为1*1，P为n*2
        tx = float(Ou[0])
        ty = float(Ou[1])
        tft_mat = np.array([
            [-math.sin(theta), -math.cos(theta), math.sin(theta) * tx + math.cos(theta) * ty],
            [math.cos(theta), -math.sin(theta), math.sin(theta) * tx - math.cos(theta) * ty],
            [0, 0, 0]
        ])
        b = []
        for temp in P:
            ex_temp = np.array([temp[0], temp[1], 1]).T
            b.append(np.dot(tft_mat, ex_temp))
        b = np.array(b)
        return b[:, 0:2]

    def setR(x, y):
        # 输入n*2，输出2n*1
        min1 = min(np.min(x[:, 0]), np.min(y[:, 0]))
        min2 = min(np.min(x[:, 1]), np.min(y[:, 1]))
        a = np.c_[(y[:, 0] - min1), y[:, 1] - min2]
        # a = a.reshape((len_P*2,1))
        return a

    def setP(x, y):
        # 输入n*2，输出2n*1
        min1 = min(np.min(x[:, 0]), np.min(y[:, 0]))
        min2 = min(np.min(x[:, 1]), np.min(y[:, 1]))
        a = np.c_[(x[:, 0] - min1), x[:, 1] - min2]
        # a = a.reshape((len_P*2,1))
        return a

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

    def setM(Theta, P, E_1):
        P = P.reshape((len_P, 2))
        Theta_P = tftmatrox(P, Theta, Ou_P)
        Theta_P = Theta_P.reshape((len_P * 2, 1))
        M = Theta_P + E_1
        return M

    def setD(R, E_3):
        D = R + E_3
        return D

    def norm_1(x):
        # 求一范数
        x = np.abs(x)
        x = np.sum(x)
        return x

    # def newMu(Mu)
    #     # 更新Mu
    #     Mu=1.2*Mu

    def newA(M, D, Y_3, Mu,labdam):
        # 更新A
        temp = np.c_[D, M]
        temp1 = np.c_[Y_3[:, 1], Y_3[:, 0]]
        Mid = np.float64(temp + temp1 / Mu)
        # 进行svd分解
        U, sigma, VT = np.linalg.svd(Mid)
        # print(sigma)
        sigma1 = sigma[1]
        sigma1_new = softmax(sigma1, labdam/Mu) ##原本是labdam/Mu=2
        sigma_new = np.r_[sigma[0], sigma1_new]
        A_new = fsvd(U, sigma_new, VT, A)
        # la = temp[:, 0].reshape((len_P, 2))
        # lo = temp[:, 1].reshape((len_P, 2))
        # plt.scatter(la[:, 0], la[:, 1], color="pink", label="D")
        # plt.scatter(lo[:, 0], lo[:, 1], color="orange", label="M")
        # print(Theta_1)



        U, sigma, VT = np.linalg.svd(A_new)
        sigma2 = sigma
        # print(sigma_new)
        H = A_new[:, 0].reshape((len_P, 2))
        g = A_new[:, 1].reshape((len_P, 2))
        # plt.scatter(H[:, 0], H[:, 1], color="red", label="A_new")
        # plt.scatter(g[:, 0], g[:, 1], color="green", label="A_new")
        # plt.show()
        # if para1 < 5:
        #     la = temp[:, 0].reshape((len_P, 2))
        #     lo = temp[:, 1].reshape((len_P, 2))
        #     plt.scatter(la[:, 0], la[:, 1], color="pink", label="D")
        #     plt.scatter(lo[:, 0], lo[:, 1], color="orange", label="M")
        #     plt.show()
        B_new = np.c_[A_new[:, 1], A_new[:, 0]]
        return B_new

    def newM(Theta_P, E_1, delta_theta, err_Theta, Y_1, A, Y_3, Mu):
        mid = A[:, 0] - Y_3[:, 1] / Mu
        mid = mid.reshape((len_P * 2, 1))
        M_new = 0.5 * (Theta_P + E_1 + delta_theta * err_Theta - Y_1 / Mu + mid)
        return M_new

    def newerr_Theta(delta_Theta, M_new, Theta_P, E_1, Y_1, Mu):
        mid = np.dot(delta_Theta.T, delta_Theta)
        mid = np.linalg.inv(mid)
        mid = np.dot(mid, delta_Theta.T)
        err_Theta_new = np.dot(mid, M_new - (Theta_P + E_1) + Y_1 / Mu)
        return err_Theta_new

    def newE_1(M, Theta_P, delta_Theta, err_Theta, Y_1, Mu, labda):
        mid = M - Theta_P - delta_Theta * err_Theta - Y_1 / Mu
        E_1_new = np.array(softmax(mid, Mu)).reshape((len_P * 2, 1))
        return E_1_new

    def newD(R, E_3, Y_2, A_new, Y_3, Mu, err_theta_1):
        mid = A_new[:, 1] - Y_3[:, 1] / Mu
        D_new = 0.5 * (R + Y_2 / Mu + E_3 + delta_Theta_1 * err_theta_1 + mid.reshape((len_P * 2, 1)))
        return D_new

    def newE_3(D, R, Y_2, Mu):
        mid = D - Theta_R - Y_2 / Mu - delta_Theta_1 * err_Theta_1
        E_3_new = np.zeros((len_P * 2, 1))
        even_sum = 0
        odd_sum = 0
        for i in range(len_P):
            even_sum = even_sum + mid[2 * i]
            odd_sum = odd_sum + mid[2 * i + 1]
        lng_mean = even_sum / len_P
        lat_mean = odd_sum / len_P
        for i in range(len_P):
            E_3_new[2 * i] = lng_mean
            E_3_new[2 * i + 1] = lat_mean
        return E_3_new

    def newY_1(Y_1, Mu, Theta_P, E_1, delta_theta, err_Theta, M):
        Y_1_new = Y_1 + Mu * ((Theta_P + E_1 + delta_theta * err_Theta) - M)
        return Y_1_new

    def newY_2(Y_2, Mu, R, E_3, D):
        Y_2_new = Y_2 + Mu * (R + E_3 - D)
        return Y_2_new

    def new_Y_3(Y_3, Mu, M, D, A):
        mid = np.c_[M, D]
        Y_3_new = Y_3 + Mu * (mid - A)
        return Y_3_new

    # 设置变量以及初始化
    len_P = np.shape(P_)[0]  # 停车点个数
    len_R = np.shape(R_)[0]  # 路链上潜在的停车点数目
    # P_ = maxminnorn(P_)
    # R_ = maxminnorn(R_)
    P_2 = P_
    # OU = [0,0]
    # Theta_list = [0,345, ]
    Theta_list = [0, ]

    err_Theta = 0
    Mu = 0.5 * len_P
    rho = 1.005

    Loss_best = len_P * 1000
    Theta_best = 0
    best_start = 0

    # Theta_P = tftmatrox(P,Theta)
    # P = P_2.reshape((2 * len_P, 1))
    # R = R.reshape((2 * len_P, 1))
    # 优化迭代
    # step1:

    for start_point in range(len_R - len_P):  # R上的位置指针
        Loss_list =[]
        times_list = []
        R = R_[start_point:start_point + len_P, :]
        R = R.reshape((len_P, 2))
        # R = maxminnorn(R)
        P = P_.reshape((len_P, 2))
        P_old = P_.reshape((len_P, 2))
        P_2 = setP(P, R)
        P = setP(P, R)  # 输入的偏移park
        R = setR(P_old, R)  # 路链的标准点
        R = R.reshape((2 * len_P, 1))
        P = P.reshape((2 * len_P, 1))
        Ou_P = getOu(P_2)
        Ou_R = getOu(R.reshape(len_P, 2))
        # 平移停车点的起点，找到最佳的停车点位置
        for Theta in Theta_list:
            Theta_1 = 0
            E_1 = np.zeros((len_P * 2, 1))
            E_3 = np.zeros((len_P * 2, 1))
            M = setM(Theta, P, E_1)
            D = setD(R, E_3)
            A = np.c_[M, D]
            Y_1 = np.zeros((len_P * 2, 1))
            Y_2 = np.zeros((len_P * 2, 1))
            Y_3 = np.zeros((len_P * 2, 2))
            err_Theta = 0
            err_Theta_1 = 0
            Mu =  10*len_P
            rho = 1
            lambda_ = 1# 根据具体情况进行改进A的核范数的权重
            Loss_old = 0
            para2 = 500  # 最大迭代次数
            # step2
            para1 = 10
            while (para1):
                delta_Theta = jacobi(Theta, P_2, Ou_P).reshape((2 * len_P, 1))
                delta_Theta_1 = jacobi(Theta_1, R.reshape((len_P, 2)), Ou_R).reshape((2 * len_P, 1))
                Theta_P = tftmatrox(P_2, Theta, Ou_P).reshape((2 * len_P, 1))
                Theta_R = tftmatrox(R.reshape((len_P, 2)), Theta_1, Ou_R).reshape((2 * len_P, 1))
                # temp_2 = Theta_P.reshape((len_P, 2))
                # plt.scatter(temp_2[:, 0], temp_2[:, 1])
                # tras = (Theta_P).reshape((len_P, 2))
                # thas = D.reshape(len_P, 2)
                # plt.scatter(tras[:, 0], tras[:, 1])
                # plt.scatter(thas[:, 0], thas[:, 1])
                # if para1 < 5:
                #     plt.show()
                A_new = newA(M, D, Y_3, Mu,lambda_)

                M_new = newM(Theta_P, E_1, delta_Theta, err_Theta, Y_1, A_new, Y_3, Mu)
                E = M_new.reshape((len_P, 2))  # M的形状
                err_Theta_new = newerr_Theta(delta_Theta, M_new, Theta_P, E_1, Y_1, Mu)
                E_1 = newE_1(M_new, Theta_P, delta_Theta, err_Theta_new, Y_1, Mu, lambda_)###正常是关的
                D_new = newD(Theta_R, E_3, Y_2, A_new, Y_3, Mu, err_Theta_1)
                err_Theta_1 = newerr_Theta(delta_Theta_1, D_new, Theta_R, E_3, Y_2, Mu)
                E_3_new = newE_3(D_new, R, Y_2, Mu)
                Theta_1 = Theta_1 + err_Theta_1
                err_Theta_1 = 0
                Theta_R = tftmatrox(R.reshape((len_P, 2)), Theta_1, Ou_R).reshape((2 * len_P, 1))
                D_new = Theta_R + E_3_new + delta_Theta_1 * err_Theta_1
                # Mu = rho * Mu
                Mu = rho * Mu*1.2#Mu无限增大提高约束
                print(f"mu={Mu}")
                M = M_new
                err_Theta = err_Theta_new
                # E_1 = E_1_new
                E_3 = E_3_new
                D = D_new
                Theta = Theta + err_Theta
                Theta_1 = Theta_1 + err_Theta_1
                # print(err_Theta)
                err_Theta = 0
                err_Theta_1 = 0
                if Theta_1 >= math.pi:
                    Theta_1 -= math.pi
                err_Theta_1 = 0
                if Theta >= math.pi:
                    Theta -= math.pi
                para1 -= 1
                Theta_P_ = tftmatrox(P_2, Theta, Ou_P).reshape((2 * len_P, 1))
                E_1_ = D - Theta_P_
                A = np.c_[M, D]
                # L = np.c_[Theta_P+E_1, D]
                U, sigma, VT = np.linalg.svd(A)
                A_rank_1 = sigma[1]
                print(A_rank_1)
                # # print(A_rank_1)
                # a_1 = np.sum(Y_1 * (Theta_P + E_1 + delta_Theta * err_Theta - D))
                # a_2 = Mu / 2 * \
                #       np.linalg.norm(np.float64(Theta_P + E_1 + delta_Theta * err_Theta - D))
                # a_3 = np.sum(Y_2 * (R + E_3 - D))
                # a_4 = norm_1(E_1, )
                # a_5 = lambda_ * A_rank_1
                Loss = norm_1(E_1_, ) + 10*lambda_ * A_rank_1 + np.sum(
                    Y_1 * (Theta_P_ + E_1 + delta_Theta * err_Theta - D)) + Mu / 2 * \
                       np.linalg.norm(np.float64(Theta_P_ + E_1 + delta_Theta * err_Theta - D)) + np.sum(
                    Y_2 * (Theta_R + E_3 - D)) + Mu / 2 * np.linalg.norm(Theta_R + E_3 - D) + np.sum(Y_3 * \
                                                                                                     (np.c_[
                                                                                                          M, D] - A)) + Mu / 2 * np.linalg.norm(
                    np.float64(np.c_[M, D] - A))

                print(Loss)
                Loss_list.append(Loss)
                times_list.append(500-para1)
            # plt.xlabel("迭代次数",fontsize = 20)
            # plt.ylabel("$loss$数值",fontsize = 20)
            # plt.plot(times_list,Loss_list)
            # plt.show()
            # Theta_P = tftmatrox(P_2, Theta, Ou_P).reshape((2 * len_P, 1))
            # E_1 = D - Theta_P
            # tras = (Theta_P).reshape((len_P,2))
            # thas = D.reshape(len_P,2)
            # plt.scatter(tras[:,0],tras[:,1])
            # plt.scatter(thas[:,0],thas[:,1])
            # plt.show()

            if Loss < Loss_best:
                Loss_best = Loss
                best_start = start_point
                Theta_best = Theta
                Theta_best_1 =Theta_1
                # print(Loss)
        # plt.plot(times_list, Loss_list)
        #         # plt.show()
            # plt.plot(times_list,Loss_list)
            # plt.show()
    # print('E_1',E_1)
    # print(E_3)
    # print(Theta)
    return best_start,Loss_best

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
    return site,2

# def md(P_, R_):
#     # 输入P为停车点的gps数组，大小为n*2，R为路链的GPS大小为m*2（m>n）
#     # L=||E_1||+lamuda||A||_(r=1)+<Y_1,theta_0.P+delta tehta(theta-tehta_0))略
#     def maxminnorn(x):
#         list_1 = []
#         list_2 = []
#         lon = x[:, 0]
#         lat = x[:, 1]
#         max_lat = np.max(lat)
#         min_lat = np.min(lat)
#         max_lon = np.max(lon)
#         min_lon = np.min(lon)
#         for i in lon:
#             t = (i - (min_lon)) / (max_lon - min_lon)
#             list_1.append(t)
#         for i in lat:
#             k = (i - (min_lat)) / (max_lat - min_lat)
#             list_2.append(k)
#         list_1 = np.array(list_1)
#         list_2 = np.array(list_2)
#         resort = np.c_[list_1, list_2]
#         return resort
#
#     def getOu(X):
#         lt = copy.copy(X[:, 1])
#         lt.sort()
#         ln = copy.copy(X[:, 0])
#         ln.sort()
#         lt_range = lt[-1] - lt[0]
#         ln_range = ln[-1] - ln[0]
#         if ln_range >= lt_range:
#             h = min(X[:, 0])
#             w = np.where(X[:, 0] == h)
#             w = np.array(w)
#             # if np.size(w) > 1:
#             w = int(w[0][0])
#             Ou = X[w]
#         if ln_range < lt_range:
#             h = min(X[:, 1])
#             w = np.where(X[:, 1] == h)
#             w = np.array(w)
#             # if len(w) > 1:
#             w = int(w[0][0])
#             Ou = X[w]
#         # r = float(Ou[:,0])
#         return Ou
#
#     def tft(theta, Ou = np.array([0, 0])):
#         # theta1*1，O为2*2
#         # 生成旋转矩阵
#
#         mateix = np.array([[math.cos(theta), -math.sin(theta),
#                             (1 - math.cos(theta)) * float(Ou[ 0]) + float(Ou[1]) * (math.sin(theta))],
#                            [math.sin(theta), math.cos(theta),
#                             (1 - math.cos(theta)) * float(Ou[ 0]) - float(Ou[1]) * (math.sin(theta))],
#                            [0, 0, 1]])
#
#         return mateix
#
#     def jacobi(theta, P, Ou=np.array([0, 0])):
#         # tehta为1*1，P为n*2
#         tx = float(Ou[0])
#         ty = float(Ou[1])
#         tft_mat = np.array([
#             [-math.sin(theta), -math.cos(theta), math.sin(theta) * tx + math.cos(theta) * ty],
#             [math.cos(theta), -math.sin(theta), math.sin(theta) * tx - math.cos(theta) * ty],
#             [0, 0, 0]
#         ])
#         b = []
#         for temp in P:
#             ex_temp = np.array([temp[0], temp[1], 1]).T
#             b.append(np.dot(tft_mat, ex_temp))
#         b = np.array(b)
#         return b[:, 0:2]
#
#     def setR(x, y):
#         # 输入n*2，输出2n*1
#         min1 = min(np.min(x[:, 0]), np.min(y[:, 0]))
#         min2 = min(np.min(x[:, 1]), np.min(y[:, 1]))
#         a = np.c_[(y[:, 0] - min1), y[:, 1] - min2]
#         # a = a.reshape((len_P*2,1))
#         return a
#
#     def setP(x, y):
#         # 输入n*2，输出2n*1
#         min1 = min(np.min(x[:, 0]), np.min(y[:, 0]))
#         min2 = min(np.min(x[:, 1]), np.min(y[:, 1]))
#         a = np.c_[(x[:, 0] - min1), x[:, 1] - min2]
#         # a = a.reshape((len_P*2,1))
#         return a
#
#     def tftmatrox(P, theta, Ou):
#         # 对坐标点进行旋转
#         # 输入n*2输出n*2
#         tft_matrix = tft(theta, Ou)
#         b = []
#         for temp in P:
#             ex_temp = np.array([temp[0], temp[1], 1]).T
#             tft_point = np.dot(tft_matrix, ex_temp)
#             b.append(tft_point)
#         b = np.array(b)
#         return b[:, 0:2]
#
#     def setM(Theta, P, E_1):
#         P = P.reshape((len_P, 2))
#         Theta_P = tftmatrox(P, Theta, Ou_P)
#         Theta_P = Theta_P.reshape((len_P * 2, 1))
#         M = Theta_P + E_1
#         return M
#
#     def setD(R, E_3):
#         D = R + E_3
#         return D
#
#     def norm_1(x):
#         # 求一范数
#         x = np.abs(x)
#         x = np.sum(x)
#         return x
#
#     def newM(Theta_P, E_1, delta_theta, err_Theta, Y_1, A, Y_3, Mu):
#         mid = D - Y_3[:, 1] / Mu
#         mid = mid.reshape((len_P * 2, 1))
#         M_new = 0.5 * (Theta_P + E_1 + delta_theta * err_Theta - Y_1 / Mu + mid)
#         return M_new
#
#     def newerr_Theta(delta_Theta, M_new, Theta_P, E_1, Y_1, Mu):
#         mid = np.dot(delta_Theta.T, delta_Theta)
#         mid = np.linalg.inv(mid)
#         mid = np.dot(mid, delta_Theta.T)
#         err_Theta_new = np.dot(mid, M_new - (Theta_P + E_1) + Y_1 / Mu)
#         return err_Theta_new
#
#     def newE_1(M, Theta_P, delta_Theta, err_Theta, Y_1, Mu, labda):
#         mid = M - Theta_P - delta_Theta * err_Theta - Y_1 / Mu
#         E_1_new = np.array(softmax(mid, 500)).reshape((len_P * 2, 1))
#         return E_1_new
#
#     def newD(R, E_3, Y_2, A_new, Y_3, Mu, err_theta_1):
#         mid = A_new[:, 1] - Y_3[:, 1] / Mu
#         D_new = 0.5 * (R + Y_2 / Mu + E_3 + delta_Theta_1 * err_theta_1 + mid.reshape((len_P * 2, 1)))
#         return D_new
#
#     def newE_3(D, R, Y_2, Mu):
#         mid = D - Theta_R - Y_2 / Mu - delta_Theta_1 * err_Theta_1
#         E_3_new = np.zeros((len_P * 2, 1))
#         even_sum = 0
#         odd_sum = 0
#         for i in range(len_P):
#             even_sum = even_sum + mid[2 * i]
#             odd_sum = odd_sum + mid[2 * i + 1]
#         lng_mean = even_sum / len_P
#         lat_mean = odd_sum / len_P
#         for i in range(len_P):
#             E_3_new[2 * i] = lng_mean
#             E_3_new[2 * i + 1] = lat_mean
#         return E_3_new
#
#     def newY_1(Y_1, Mu, Theta_P, E_1, delta_theta, err_Theta, M):
#         Y_1_new = Y_1 + Mu * ((Theta_P + E_1 + delta_theta * err_Theta) - M)
#         return Y_1_new
#
#     def newY_2(Y_2, Mu, R, E_3, D):
#         Y_2_new = Y_2 + Mu * (R + E_3 - D)
#         return Y_2_new
#
#     def new_Y_3(Y_3, Mu, M, D, A):
#         mid = np.c_[M, D]
#         Y_3_new = Y_3 + Mu * (mid - A)
#         return Y_3_new
#
#     # 设置变量以及初始化
#     len_P = np.shape(P_)[0]  # 停车点个数
#     len_R = np.shape(R_)[0]  # 路链上潜在的停车点数目
#     # P_ = maxminnorn(P_)
#     # R_ = maxminnorn(R_)
#     P_2 = P_
#     # OU = [0,0]
#     # Theta_list = [0,345, ]
#     Theta_list = [0, ]
#
#     err_Theta = 0
#     Mu = 0.5 * len_P
#     rho = 1.005
#     lambda_ = 10000  # 根据具体情况进行改进A的核范数的权重
#     Loss_best = len_P * 1000
#     Theta_best = 0
#     best_start = 0
#
#     # 优化迭代
#     # step1:
#
#     for start_point in range(len_R - len_P):  # R上的位置指针
#         Loss_list =[]
#         times_list = []
#         R = R_[start_point:start_point + len_P, :]
#         R = R.reshape((len_P, 2))
#         # R = maxminnorn(R)
#         P = P_.reshape((len_P, 2))
#         P_old = P_.reshape((len_P, 2))
#         P_2 = setP(P, R)
#         P = setP(P, R)  # 输入的偏移park
#         R = setR(P_old, R)  # 路链的标准点
#         R = R.reshape((2 * len_P, 1))
#         P = P.reshape((2 * len_P, 1))
#         Ou_P = getOu(P_2)
#         Ou_R = getOu(R.reshape(len_P, 2))
#         # 平移停车点的起点，找到最佳的停车点位置
#         for Theta in Theta_list:
#             Theta_1 = 0
#             E_1 = np.zeros((len_P * 2, 1))
#             E_3 = np.zeros((len_P * 2, 1))
#             M = setM(Theta, P, E_1)
#             D = setD(R, E_3)
#             A = np.c_[M, D]
#             Y_1 = np.zeros((len_P * 2, 1))
#             Y_2 = np.zeros((len_P * 2, 1))
#             Y_3 = np.zeros((len_P * 2, 2))
#             err_Theta = 0
#             err_Theta_1 = 0
#             Mu =  10*len_P
#             rho = 1
#             lambda_ = 5000
#             Loss_old = 0
#             para2 = 500  # 最大迭代次数
#             # step2
#             para1 = 500
#             while (para1):
#                 delta_Theta = jacobi(Theta, P_2, Ou_P).reshape((2 * len_P, 1))
#                 delta_Theta_1 = jacobi(Theta_1, R.reshape((len_P, 2)), Ou_R).reshape((2 * len_P, 1))
#                 Theta_P = tftmatrox(P_2, Theta, Ou_P).reshape((2 * len_P, 1))
#                 Theta_R = tftmatrox(R.reshape((len_P, 2)), Theta_1, Ou_R).reshape((2 * len_P, 1))
#                 M_new = newM(Theta_P, E_1, delta_Theta, err_Theta, Y_1, A, Y_3, Mu)
#                 E = M_new.reshape((len_P, 2))  # M的形状
#                 err_Theta_new = newerr_Theta(delta_Theta, M_new, Theta_P, E_1, Y_1, Mu)
#                 # E_1_new = newE_1(M_new, Theta_P, delta_Theta, err_Theta_new, Y_1, Mu, lambda_)
#                 D_new = newD(Theta_R, E_3, Y_2, A_new, Y_3, Mu, err_Theta_1)
#                 err_Theta_1 = newerr_Theta(delta_Theta_1, D_new, Theta_R, E_3, Y_2, Mu)
#                 E_3_new = newE_3(D_new, R, Y_2, Mu)
#                 Theta_1 = Theta_1 + err_Theta_1
#                 err_Theta_1 = 0
#                 Theta_R = tftmatrox(R.reshape((len_P, 2)), Theta_1, Ou_R).reshape((2 * len_P, 1))
#                 D_new = Theta_R + E_3_new + delta_Theta_1 * err_Theta_1
#                 Mu = rho * Mu
#                 M = M_new
#                 err_Theta = err_Theta_new
#                 # E_1 = E_1_new
#                 E_3 = E_3_new
#                 D = D_new
#                 Theta = Theta + err_Theta
#                 Theta_1 = Theta_1 + err_Theta_1
#                 # print(err_Theta)
#                 err_Theta = 0
#                 err_Theta_1 = 0
#                 if Theta_1 >= math.pi:
#                     Theta_1 -= math.pi
#                 err_Theta_1 = 0
#                 if Theta >= math.pi:
#                     Theta -= math.pi
#                 para1 -= 1
#                 Theta_P_ = tftmatrox(P_2, Theta, Ou_P).reshape((2 * len_P, 1))
#                 E_1_ = D - Theta_P_
#                 A = np.c_[M, D]
#                 # L = np.c_[Theta_P+E_1, D]
#                 U, sigma, VT = np.linalg.svd(A)
#                 A_rank_1 = sigma[1]
#                 print(A_rank_1)
#                 # # print(A_rank_1)
#                 # a_1 = np.sum(Y_1 * (Theta_P + E_1 + delta_Theta * err_Theta - D))
#                 # a_2 = Mu / 2 * \
#                 #       np.linalg.norm(np.float64(Theta_P + E_1 + delta_Theta * err_Theta - D))
#                 # a_3 = np.sum(Y_2 * (R + E_3 - D))
#                 # a_4 = norm_1(E_1, )
#                 # a_5 = lambda_ * A_rank_1
#                 Loss = norm_1(E_1_, ) + 10*lambda_ * A_rank_1 + np.sum(
#                     Y_1 * (Theta_P_ + E_1 + delta_Theta * err_Theta - D)) + Mu / 2 * \
#                        np.linalg.norm(np.float64(Theta_P_ + E_1 + delta_Theta * err_Theta - D)) + np.sum(
#                     Y_2 * (Theta_R + E_3 - D)) + Mu / 2 * np.linalg.norm(Theta_R + E_3 - D) + np.sum(Y_3 * \
#                                                                                                      (np.c_[
#                                                                                                           M, D] - A)) + Mu / 2 * np.linalg.norm(
#                     np.float64(np.c_[M, D] - A))
#
#                 print(Loss)
#                 Loss_list.append(Loss)
#                 times_list.append(500-para1)
#             # plt.xlabel("迭代次数",fontsize = 20)
#             # plt.ylabel("$loss$数值",fontsize = 20)
#             # plt.plot(times_list,Loss_list)
#             # plt.show()
#             # Theta_P = tftmatrox(P_2, Theta, Ou_P).reshape((2 * len_P, 1))
#             # E_1 = D - Theta_P
#             # tras = (Theta_P).reshape((len_P,2))
#             # thas = D.reshape(len_P,2)
#             # plt.scatter(tras[:,0],tras[:,1])
#             # plt.scatter(thas[:,0],thas[:,1])
#             # plt.show()
#
#             if Loss < Loss_best:
#                 Loss_best = Loss
#                 best_start = start_point
#                 Theta_best = Theta
#                 Theta_best_1 =Theta_1
#                 # print(Loss)
#         # plt.plot(times_list, Loss_list)
#         #         # plt.show()
#             # plt.plot(times_list,Loss_list)
#             # plt.show()
#     return best_start,Loss_best


if __name__ == '__main__':
    true_list = []
    precision = 0
    num = 0
    long_len = 0
    n=10
    mu=0.98
    R_list = np.load("road.npy",allow_pickle=True)
    P_list = np.load("park.npy",allow_pickle=True)
    P_T = np.load("gt.npy",allow_pickle=True)
    curse_list = [0,4,9,12,13,17,21,22,25,27]
    #
    for index in range(51):
    # for index in curse_list:
    #     if index in curse_list:
    #         continue
        n+=1
        R = R_list[index]
        P = P_list[index]
        P_th = P_T[index]
    # R = np.array([[116.36451199999962, 39.86813945454547, ],
    #               [116.36466399999924, 39.86813254545458, ],
    #               [116.36481599999885, 39.868125636363686, ],
    #               [116.36496799999847, 39.868118727272794, ],
    #               [116.36511999999809, 39.86811181818191, ],
    #               [116.3652719999977, 39.86812039999954, ],
    #               [116.36542499999732, 39.86812275862088, ],
    #               [116.36557699999693, 39.86811227586228, ],
    #               [116.36572999999655, 39.86811727272706, ],
    #               [116.36588199999616, 39.868126484848254, ],
    #               [116.36603499999578, 39.86812512820534, ],
    #               [116.36618699999539, 39.86811733333357, ],
    #               [116.36633899999501, 39.86811, ],
    #               [116.36649199999462, 39.86811, ],
    #               [116.36664499999424, 39.868113166666475, ],
    #               [116.36679799999385, 39.86811826666646, ],
    #               [116.36695099999346, 39.86812309090869, ],
    #               [116.36710299999308, 39.86813230302988, ],
    #               [116.3672549999927, 39.86814, ],
    #               [116.36740799999231, 39.86814, ],
    #               [116.36756099999192, 39.86814, ],
    #               [116.36771399999154, 39.86814335483844, ],
    #               [116.36786699999115, 39.868148290322296, ],
    #               [116.36801899999077, 39.868155436572806, ],
    #               [116.36817099999038, 39.868163783634834, ],
    #               [116.36832299999, 39.86817170250066, ],
    #               [116.36847499998962, 39.868178372092565, ],
    #               [116.36862699998923, 39.86818504168448, ],
    #               [116.36877899998885, 39.86819149999957, ],
    #               [116.36893099998846, 39.8681973461534, ],
    #               [116.36908399998808, 39.8682, ],
    #               [116.36923699998769, 39.8682, ],
    #               [116.3693899999873, 39.86820166666614, ],
    #               [116.36954199998692, 39.868207999999456, ],
    #               [116.36969399998654, 39.86820013793057, ],
    #               [116.36984699998615, 39.86820541379262, ],
    #               [116.36999899998577, 39.86821071698059, ],
    #               [116.37015099998538, 39.868216452829635, ],
    #               [116.370302999985, 39.86822218867868, ],
    #               [116.37045499998462, 39.868227924527716, ],
    #               [116.37060699998423, 39.868233592592006, ],
    #               [116.37075899998385, 39.868239222221625, ],
    #               [116.37091099998347, 39.868244851851244, ],
    #               [116.37106399998308, 39.86825, ],
    #               [116.3712129999827, 39.86822562501081, ],
    #               [116.37127399998255, 39.8681160001483, ],
    #               [116.37128799998251, 39.86799700014861, ],
    #               [116.37130199998248, 39.86787800014892, ],
    #               [116.37131599998244, 39.867759000149235, ],
    #               [116.37132999998241, 39.86764000014954, ],
    #               [116.37134399998237, 39.867521886815375, ],
    #               [116.37135799998234, 39.867403773482316, ],
    #               ])
    #
    # P = np.array([[116.36908399998808, 39.8682, ],
    #               [116.36923899998769, 39.86822, ],
    #               [116.3693899999873, 39.86823166666614, ],
    #               [116.36954199998692, 39.868457999999456, ],
    #               [116.36968399998654, 39.86834013793057, ],
    #               [116.36985699998615, 39.86820541379262, ],
    #               [116.36999899998577, 39.86821071698059, ],
    #               [116.37015099998538, 39.868216452829635, ],
    #               [116.370302999985, 39.86822218867868, ],
    #               [116.37045499998462, 39.868227924527716, ],
    #               [116.37060699998423, 39.868243592592006, ],
    #               [116.37075899998385, 39.868239222221625, ],
    #               [116.37091199998347, 39.868244851851244, ],
    #               [116.37106359998308, 39.86865, ],
    #               [116.3712122999827, 39.86852562501081, ],
    #               [116.37127399998255, 39.8681160001483, ],
    #               [116.37128799998251, 39.86799700014861, ],
    #               [116.371301129998248, 39.86757800014892, ],
    #               [116.37131599998244, 39.867759000149235, ],
    #               [116.37133599998241, 39.86764000014954, ],
    #               [116.371343899998237, 39.867521886815375, ],
    #               [116.37133789998234, 39.867403773482316, ],
    #               ])
    # P_old = copy.copy(P)
        lon = copy.copy(R[:, 0])
        lat = copy.copy(R[:, 1])
        min_lon = np.min(lon)
        min_lat = np.min(lat)
        len_P = len(P)
        len_R = len(R)
        # long_len += len_P
    # P = initial(P)  # 输入的偏移park
    # R = initial(R)
    # P = tftmatrox(P, math.pi * -15 / 180, [0, 0])
    # P = P + [0.002, -0.0001]
    # P += [min_lon,min_lat]
    # R += [min_lon,min_lat]
    # s施加干扰
    #     np.random.seed(999)
    #     a = np.random.random((len_P,1))/5000      #0.0002 and  0.0005
    #     b = np.random.random((len_P,1))/5000
    #     b = np.zeros((len_P,1))
    #     c = np.c_[a,b]
    #     P = P+a

    # wt.writetxtred(R,'干扰1平移旋转.txt')
    # wt.writetxtblue(P,'干扰1平移旋转.txt')



        # plt.plot(R[:,0],R[:,1],label = "predicted parking spaces",c="r",linewidth=6)
        # plt.scatter(P[:,0],P[:,1],label = "collected　parking　spaces",c = "b")
        # plt.ylim(min_lat-0.0015,min_lat+0.003)
        # plt.xlim(min_lon-0.0006,min_lon+0.007)
        # plt.legend(fontsize = 20)
        # plt.show()

        best_start,Loss_best=admm(P, R)
        # plt.scatter(R[:, 0], R[:, 1],label = "predicted parking spaces",c = "r")
        best_park_GPS = R[best_start:best_start + len_P, :]
        true_list.append(best_park_GPS)


    # wt.writetxtred(R,'干扰2平移旋转后.mif')
    # wt.writetxtblue(P,'干扰2平移旋转后.mif')
    # wt.writetxtblack(best_park_GPS,'干扰2平移旋转后.mif')
    #     plt.scatter(P[:,0],P[:,1],label = "collected　parking　spaces",c = "b")
    #     plt.scatter(best_park_GPS[:,0],best_park_GPS[:,1],c = "k",label = "matched parking spaces")
    #     # plt.ylim(min_lat-0.0015,min_lat+0.003)
    #     # plt.xlim(min_lon-0.0015,min_lon+0.007)
    #     plt.legend(fontsize = 20)
    #     plt.savefig('C:\\Users\\BJL\\Desktop\\使用图\\'+str(index)+'.svg', format='svg', bbox_inches='tight')
    #     plt.close()
        # plt.show()

        #基于欧氏距离
        # P = P.reshape(2*len_P,1)
        # R = R.reshape(2*len_R,1)
        # best_site, err = getsite(P, R)
        # R = R.reshape(len_R,2)
        # P = P.reshape(len_P,2)
        # best_park_GPS = R[int(best_site / 2):int(best_site / 2 + len_P), ].copy()
        # # plt.scatter(R[:, 0], R[:, 1],label = "predicted parking spaces",c = "r")
        # best_park_GPS = best_park_GPS.reshape(len_P,2)
        # plt.scatter(P[:,0],P[:,1],label = "collected　parking　spaces",c = "b")
        # plt.scatter(best_park[:,0],best_park[:,1],c = "k",label = "matched parking spaces")
        # # plt.ylim(-0.0015,0.007)
        # # plt.xlim(-0.0015,0.007)
        # plt.legend(fontsize = 20)
        # plt.show()
        long_len += len_P*mu
        a = np.mean(np.abs(best_park_GPS-P_th))
        if len(best_park_GPS)==len(P_th):
            for item in range(len(P_th)):
                if best_park_GPS[item] in P_th:
                    num += 1
        else:
            print(index)
            break
        precision +=a
    num_av = num/long_len
    num_per = num/11
    #num_per = num /11
    precision = gps_distance_google.do(precision / n)
    print('定位准确度',precision)
    print("准确数目：",num,"准确率：",num_av)

    precision = precision/51
    #precision = precision/len(curse_list)
    print(precision)
    # np.save("true",true_list,allow_pickle=True)
#只进行填充的





