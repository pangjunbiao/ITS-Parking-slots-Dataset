# 导入sympy包，用于求导，方程组求解等等
from sympy import *
import numpy as np
import math
# import tftmatrox
from S_t import softmax
from tftmatrox import transform
from shape import fsvd
# import read21q2csv
# import readxls

# def setE(I,D):
#     x = np.min(I[:,0],D[:,0])
#     y = np.min(I[:,1],D[:,1])
#     E1 = np.full((np.shape(I)[0],1),x)
#     E2 = np.full((np.shape(I)[0],1),y)
#     return E
def admm(P,R_):
    #输入P为停车点的gps数组，大小为n*2，R为路链的GPS大小为m*2（m>n）
    #L=||E_1||+lamuda||A||_(r=1)+<Y_1,theta_0.P+delta tehta(theta-tehta_0))略
    def tft(theta, O):
        #theta1*1，O为2*2
        # 生成旋转矩阵

        mateix = np.array([[math.cos(theta), -math.sin(theta),0],
                           [math.sin(theta), math.cos(theta), 0],
                           [0, 0, 1]])

        return mateix

    def jacobi(theta,P):
        #tehta为1*1，P为n*2
        tft_mat = np.array([
            [math.sin(theta),math.cos(theta),0],
            [-math.cos(theta),math.sin(theta),0],
            [0,0,0]
        ])
        b = []
        for temp in P:
            ex_temp = np.array([temp[0], temp[1], 1]).T
            b.append(np.dot(tft_mat,ex_temp))
        b = np.array(b)
        return b[:, 0:2]

    def setR(x,y):
        #输入n*2，输出2n*1
        min1 = min(np.min(x[:,0]),np.min(y[:,0]))
        min2 = min(np.min(x[:,1]),np.min(y[:,1]))
        a = np.c_[(y[:,0]-min1),y[:,1]-min2]
        # a = a.reshape((len_P*2,1))
        return a

    def setP(x,y):
        #输入n*2，输出2n*1
        min1 = min(np.min(x[:,0]),np.min(y[:,0]))
        min2 = min(np.min(x[:,1]),np.min(y[:,1]))
        a = np.c_[(x[:,0]-min1),x[:,1]-min2]
        # a = a.reshape((len_P*2,1))
        return a

    def tftmatrox(P,theta):
        #对坐标点进行旋转
        #输入n*2输出n*2
        tft_matrix = tft(theta, OU)
        b = []
        for temp in P :
            ex_temp = np.array([temp[0],temp[1],1]).T
            tft_point = np.dot(tft_matrix,ex_temp)
            b.append(tft_point)
        b = np.array(b)
        return b[:,0:2]

    def setM(Theta,P,E_1):
        P = P.reshape((len_P,2))
        Theta_P = tftmatrox(P,Theta)
        Theta_P = Theta_P.reshape((len_P*2,1))
        M = Theta_P+E_1
        return M

    def setD(R,E_3):
        D = R+E_3
        return D

    def norm_1(x):
        #求一范数
        x = np.abs(x)
        x= np.sum(x)
        return x

    def newA(M,D,Y_3,Mu):
        #更新A
        Mid = np.float64(np.c_[M,D]+Y_3/Mu)
        # 进行svd分解
        U, sigma, VT = np.linalg.svd(Mid)
        sigma1 =sigma[1]
        sigma1_new = softmax(sigma1, Mu)
        sigma_new = np.r_[sigma[0],sigma1_new]
        A_new = fsvd(U, sigma_new, VT, A)
        return  A_new

    def newM(Theta_P,E_1,delta_theta,err_Theta,Y_1,A,Y_3,Mu):
        mid = A[:, 0] - Y_3[:, 1] / Mu
        mid = mid .reshape((50,1))
        M_new = 0.5*(Theta_P+E_1+delta_theta*err_Theta+Y_1/Mu+mid)
        return M_new

    def newerr_Theta(delta_Theta,M_new,Theta_P,E_1,Y_1,Mu):
        mid = np.dot(delta_Theta.T,delta_Theta)
        mid = np.linalg.inv(mid)
        mid = np.dot(mid,delta_Theta.T)
        err_Theta_new = np.dot(mid,M_new-(Theta_P+E_1-Y_1/Mu))
        return err_Theta_new

    def newE_1(M,Theta_P,delta_Theta,err_Theta,Y_1,Mu):
        mid = M-Theta_P-delta_Theta*err_Theta-Y_1/Mu
        E_1_new = np.array(softmax(mid,Mu)).reshape((len_P*2,1))
        return E_1_new

    def newD(R,E_3,Y_2,A_new,Y_3,Mu):
        mid = A_new[:, 1] + Y_3[:, 1] / Mu
        D_new = 0.5*(R+Y_2/Mu +mid .reshape((50,1)))
        return D_new

    def newE_3(D,R,Y_2,Mu):
        mid = D-R-Y_2/Mu
        E_3_new = np.zeros((len_P*2,1))
        even_sum = 0
        odd_sum = 0
        for i in range(len_P) :
            even_sum = even_sum + mid[2*i]
            odd_sum = odd_sum + mid[2*i+1]
        lng_mean = even_sum/len_P
        lat_mean = odd_sum/len_P
        for i in range(len_P):
            E_3_new[2*i] = lng_mean
            E_3_new[2*i+1] = lat_mean
        return E_3_new

    def newY_1(Y_1,Mu,Theta_P,E_1,delta_theta,err_Theta,M):
        Y_1_new = Y_1+Mu*((Theta_P+E_1+delta_theta*err_Theta)-M)
        return Y_1_new

    def newY_2(Y_2,Mu,R,E_3,D):
        Y_2_new = Y_2+Mu*(R+E_3-D)
        return Y_2_new

    def new_Y_3(Y_3,Mu,M,D,A):
        mid = np.c_[M,D]
        Y_3_new = Y_3+Mu*(mid-A)
        return Y_3_new

    # 设置变量以及初始化
    len_P = np.shape(P)[0] #停车点个数
    len_R = np.shape(R_)[0] #路链上潜在的停车点数目
    P_2 = P
    OU = [0,0]
    Theta_list = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,]

    err_Theta = 0
    Mu = 4*len_P
    rho = 1.12
    lambda_ = 10000 #根据具体情况进行改进A的核范数的权重
    Loss_best = len_P*1000
    Theta_best = 0
    best_start = 0

    # Theta_P = tftmatrox(P,Theta)
    # P = P_2.reshape((2 * len_P, 1))
    # R = R.reshape((2 * len_P, 1))
    # 优化迭代
    #step1:
    for start_point in range(len_R-len_P): #R上的位置指针
        R = R_[start_point:start_point + len_P, :]
        R = R.reshape((len_P,2))
        P_ = P.reshape((len_P,2))
        P = setP(P_, R)  # 输入的偏移park
        P_2 = P
        R = setR(P_, R)  # 路链的标准点
        R = R.reshape((2 * len_P, 1))
        P = P.reshape((2*len_P,1))
        # 平移停车点的起点，找到最佳的停车点位置
        for Theta in Theta_list:
            E_1 = np.zeros((len_P * 2, 1))
            E_3 = np.zeros((len_P * 2, 1))
            M = setM(Theta, P, E_1)
            D = setD(R, E_3)
            A = np.c_[M, D]
            Y_1 = np.zeros((len_P * 2, 1))
            Y_2 = np.zeros((len_P * 2, 1))
            Y_3 = np.zeros((len_P * 2, 2))
            err_Theta = 0
            # delta_Theta = jacobi(Theta, P).reshape((2 * len_p, 1))
            Mu = 1000 * len_P
            rho = 1.12
            lambda_ = 10000
            Loss_old = 0
            para2 = 200  # 最大迭代次数
            #step2
            while(para2):
                delta_Theta = jacobi(Theta, P_2).reshape((2 * len_P, 1))
                Theta_P = tftmatrox(P_2,Theta).reshape((2 * len_P, 1))
                A_new = newA(M,D,Y_3,Mu)
                M_new = newM(Theta_P,E_1,delta_Theta,err_Theta,Y_1,A,Y_3,Mu)
                err_Theta_new =newerr_Theta(delta_Theta,M_new,Theta_P,E_1,Y_1,Mu)
                E_1_new = newE_1(M_new,Theta_P,delta_Theta,err_Theta_new,Y_1,Mu)
                D_new = newD(R,E_3,Y_2,A_new,Y_3,Mu)
                E_3_new = newE_3(D,R,Y_2,Mu)
                Y_1 = newY_1(Y_1,Mu,Theta_P,E_1_new,delta_Theta,err_Theta_new,M_new)
                Y_2 = newY_2(Y_2,Mu,R,E_3_new,D_new)
                Y_3 = new_Y_3(Y_3,Mu,M_new,D_new,A_new)
                Mu = rho*Mu
                A = A_new
                M = M_new
                err_Theta = err_Theta_new
                E_1 = E_1_new
                E_3 = E_3_new
                D = D_new
                U, sigma, VT = np.linalg.svd(A)
                A_rank_1 = sigma[1]
                # print(A_rank_1)
                Loss = norm_1(E_1,)+lambda_*A_rank_1+np.sum(Y_1*(Theta_P+E_1+delta_Theta*err_Theta-M))+Mu/2*\
                       np.linalg.norm(np.float64(Theta_P+E_1+delta_Theta*err_Theta-M))+np.sum(Y_2*(R+E_3-D))+Mu/2*np.linalg.norm(R+E_3-D)+np.sum(Y_3*\
                       (np.c_[M,D]-A))+Mu/2*np.linalg.norm(np.float64(np.c_[M,D]-A))
                print(Loss)
                Theta = Theta+err_Theta
                err_Loss = Loss-Loss_old
                Loss_old = Loss
                if Loss < Loss_best:
                    Loss_best = Loss
                    best_start = start_point
                    Theta_best =Theta
                if abs(err_Loss) < len_P*0.0001:
                    break
                para2 -= 1
            print("角度",Theta)
    print(best_start,Theta_best,Loss_best)
if __name__ == '__main__':
    R = np.array([[116.3465,39.90948  ],
         [116.34629,39.90948],
         [116.34629,39.90948  ],
         [116.3470762,39.90948  ],
         [116.3465     ,39.90948  ],
         [116.3465    , 39.90948  ],
         [116.34718    ,39.90948  ],
         [116.3470762 , 39.90948  ],
         [116.3470762  ,39.90948  ],
         [116.34772   , 39.90947  ],
         [116.34718    ,39.90948  ],
         [116.34718    ,39.90948  ],
         [116.34819   , 39.90946  ],
         [116.34772  ,  39.90947  ],
         [116.34772  ,  39.90947  ],
         [116.3483808 , 39.90946  ],
         [116.34819  ,  39.90946  ],
         [116.34819  ,  39.90946  ],
         [116.34852  ,  39.90946  ],
         [116.3483808 , 39.90946  ],
         [116.3483808  ,39.90946  ],
         [116.34915   , 39.90945  ],
         [116.34852   , 39.90946  ],
         [116.34852   , 39.90946  ],
         [116.35031   , 39.90944  ],
         [116.3496    , 39.90945  ],
         [116.34915   , 39.90945  ],
         [116.34915   , 39.90945  ],
         [116.35053   , 39.90944  ],
         [116.35031   , 39.90944  ],
         [116.35031   , 39.90944  ],
         [116.35091   , 39.90944  ],
         [116.35053   , 39.90944  ],
         [116.35053   , 39.90944  ],
         [116.35108   , 39.90944  ],
         [116.35091   , 39.90944  ],
         [116.35091   ,39.90944  ],
         [116.35123   , 39.90944  ],
         [116.35108   , 39.90944  ],
         [116.35108   , 39.90944  ],
         [116.35165   , 39.90944  ],
         [116.35123   , 39.90944  ],
         [116.35123   , 39.90944  ],
         [116.3517    , 39.90944  ],
         [116.35165   , 39.90944  ],
         [116.35165   , 39.90944  ],
         [116.35265  ,  39.90944  ],
         [116.3517   ,  39.90944  ],
         [116.3517   ,  39.90944  ]])

    P = np.array([[116.35235656181 , 39.90948156526408 , ],
        [116.35258426052437 , 39.909480107914135 , ],
        [116.35281197254514 , 39.90947861176046 , ],
        [116.35303969774783 , 39.90947707716565 , ],
        [116.35326743600623 , 39.90947550449771 , ],
        [116.35349518719207 , 39.90947389413006 , ],
        [116.35372295117541 , 39.90947224644137 , ],
        [116.35395072782453 , 39.90947056181567 , ],
        [116.35417851700576 , 39.90946884064209 , ],
        [116.35440631858386 , 39.90946708331501 , ],
        [116.3546341324217 , 39.909465290233875 , ],
        [116.35486195838045 , 39.90946346180317 , ],
        [116.3550897963196 , 39.90946159843236 , ],
        [116.35531764609696 , 39.909459700535876 , ],
        [116.35554550756866 , 39.90945776853299 , ],
        [116.35577338058911 , 39.9094558028478 , ],
        [116.35600126501119 , 39.90945380390913 , ],
        [116.35622916068611 , 39.90945177215055 , ],
        [116.35645706746354 , 39.90944970801021 , ],
        [116.35668498519154 , 39.90944761193085 , ],
        [116.35691291371664 , 39.90944548435971 , ],
        [116.35714085288384 , 39.909443325748484 , ],
        [116.35736880253667 , 39.90944113655325 , ],
        [116.35759676251715 , 39.909438917234375 , ],
        [116.35782473266586 , 39.909436668256525 , ],
        ])
    admm(P,R)




