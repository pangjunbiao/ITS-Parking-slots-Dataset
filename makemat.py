import numpy as np
from line import line

def take1 (impt,matrox):
    m = 0 # 横坐标位置指针
    n = 0 #纵坐标位置指针
    p = 0 #路链gps点指针
    f = 0 # 标 志
    while(True):
        f = 0
        for i in a :
            if impt[p,0] == i :
                for j in b :
                    if impt[p,1] == j:
                        matrox[m,n] = 2
                        p += 1
                        f=1
                        break
                    n += 1
                if f == 1:
                    break
        m +=1
    return matrox

def makem(xu,yu):
    min1 = min(np.min(xu[:,0]),np.min(yu[:,0]))
    min2 = min(np.min(xu[:,1]),np.min(yu[:,1]))
    max1 = max(np.max(xu[:,0]),np.max(yu[:,0]))
    max2 = max(np.max(xu[:,1]),np.max(yu[:,1]))
    a = np.arange(min1,max1,0.000005)#生成横坐标
    b = np.arange(min2,max2,0.000005)#生成纵坐标
    matrox1 = np.ones((np.size(a),np.size(b)))
    matrox2 = np.ones((np.size(a),np.size(b)))
    # park = take1(xu,matrox)`
    p = 0 #路链gps点指针

    while(p < np.size(xu)/2):
        f = 0 # 标 志
        m = 0  # 横坐标位置指针
        n = 0  # 纵坐标位置指针
        for i in range(np.size(a)) :
            if ((i == np.size(a)-1) or (xu[p,0] >= a[i] and xu[p,0] <= a[i+1])):
                for j in range(np.size(b)) :
                    if ((j == np.size(b)-1) or (xu[p,1] >= b[j] and xu[p,1] <= b[j+1])):
                        matrox1[m,n] = 1
                        # print(m,n)
                        p += 1
                        f=1
                    if f ==1:
                        break
                    n += 1
            if f == 1:
                break
            m +=1
    p = 0
    while (p < np.size(yu) / 2):
        f = 0  # 标 志
        m = 0  # 横坐标位置指针
        n = 0  # 纵坐标位置指针
        for i in range(np.size(a)):
            if ((i == np.size(a) - 1) or (yu[p, 0] >= a[i] and yu[p, 0] <= a[i + 1])):
                for j in range(np.size(b)):
                    if ((j == np.size(b) - 1) or (yu[p, 1] >= b[j] and yu[p, 1] <= b[j + 1])):
                        matrox2[m, n] = 1
                        # print(m,n)
                        p += 1
                        f = 1
                    if f == 1:
                        break
                    n += 1
            if f == 1:
                break
            m += 1
    return matrox1,matrox2







if __name__ == '__main__':
    lon = np.loadtxt('zjzlng.txt', delimiter=',')
    lat = np.loadtxt('zjzlat.txt', delimiter=',')
    str = np.array(line(lon, lat))
    park_lat = np.loadtxt('parklng.txt', delimiter=',')
    park_lon = np.loadtxt('parklat.txt', delimiter=',')
    park_gps = np.c_[park_lon,park_lat]
    a ,b= makem(park_gps,str)