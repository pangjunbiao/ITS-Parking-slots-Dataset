import numpy as np
import line
import matplotlib.pyplot as plt


# site 确定的停车点起点
# Err为停车点偏差

def distence (xu,yu):
    distence_sum = 0
    for i in range(np.size(xu)):
        distence_temp = xu[i]-yu[i]
        distence_sum += distence_temp**2
    return distence_sum

def getsite (xu,yu):
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

if __name__ == '__main__':
    lon = np.loadtxt('xbhnllon.txt', delimiter=',')
    lat = np.loadtxt('xbhnllat.txt', delimiter=',')
    road_gps = np.array(line.line(lon, lat))

    park_lat = np.loadtxt('xbhnlparklat.txt', delimiter=',')
    park_lon = np.loadtxt('xbhnlparklon.txt', delimiter=',')
    park_gps = np.c_[park_lon, park_lat]
    park_gps_1 = np.reshape(park_gps,(np.size(park_gps),1))
    road_gps_1 = np.reshape(road_gps,(np.size(road_gps),1))
    best_site,err = getsite(park_gps_1,road_gps_1)
    best_park = road_gps[int(best_site/2):int(best_site/2+np.size(park_gps)/2),]
    plt.plot(road_gps[:,0],road_gps[:,1],label="road")
    plt.scatter(park_gps[:,0],park_gps[:,1],color='r',label='oldpark')
    plt.legend()
    plt.show()
    plt.scatter(best_park[:,0],best_park[:,1],color='b',label='newpark')
    plt.plot(road_gps[:,0],road_gps[:,1],label="road")
    plt.scatter(park_gps[:,0],park_gps[:,1],color='r',label='oldpark')
    plt.legend()
    plt.show()
