from gps_distance_google import get_distance
import numpy as np
import ALm
import matplotlib.pyplot as plt
from tftmatrox import transform
import err

def line(lon,lat):
    #生成间隔6米的Gps路链点
    j=0
    i=1
    road_park = []
    while (True) :
        if get_distance(lon[j],lat[j],lon[i],lat[i]) >= 13.7 :
            road_park.append([lon[i],lat[i]])
            j = i
        i += 1
        if i == np.size(lon):
            break
    return road_park
if __name__ == '__main__':
    lon = np.loadtxt('zjzlng.txt', delimiter=',')
    lat = np.loadtxt('zjzlat.txt', delimiter=',')
    str = np.array(line (lon,lat))

    park_lat = np.loadtxt('parklng.txt', delimiter=',')
    park_lon = np.loadtxt('parklat.txt', delimiter=',')
    park_gps = np.c_[park_lon,park_lat]
    print("park",park_gps)

    print(np.shape(park_gps))
    print(str)
    # D,Theta_I,E = ALm.ALM(park_gps,str)
    # plt.scatter(Theta_I[:,0],Theta_I[:,1])
    # plt.scatter(park_gps[:,0],park_lat)
    # plt.show()
