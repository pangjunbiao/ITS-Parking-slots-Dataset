#encoding=utf-8  
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

#自定义函数 e指数形式
def func(x, a,u, sig):
    return  a*(np.exp(-(x - u) ** 2 /(2* sig **2))/(math.sqrt(2*math.pi)*sig))*(431+(4750/x))


#定义x、y散点坐标
x = [40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135]
x=np.array(x)
# x = np.array(range(20))
print('x is :\n',x)
num = [536,529,522,516,511,506,502,498,494,490,487,484,481,478,475,472,470,467,465,463]
y = np.array(num)
print('y is :\n',y)

popt, pcov = curve_fit(func, x, y,p0=[3.1,4.2,3.3])
#获取popt里面是拟合系数
a = popt[0]
u = popt[1]
sig = popt[2]


yvals = func(x,a,u,sig) #拟合y值
print(u'系数a:', a)
print(u'系数u:', u)
print(u'系数sig:', sig)

#绘图
plot1 = plt.plot(x, y, 's',label='original values')
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=4) #指定legend的位置右下角
plt.title('curve_fit')
plt.show()
