import numpy as np
def getmin_set(a,b):
    sum_a = 0
    for i in a :
        min_j = 99999
        for j in b :
            temp = (i[0] - j[0])+(i[1]-j[1])
            if temp < min_j:
                min_j =temp
            sum_a+=min_j*min_j
    return sum_a

def chamferdistance(a,b):
    sum_a = getmin_set(a,b)
    sum_b = getmin_set(b,a)
    return sum_a+sum_b