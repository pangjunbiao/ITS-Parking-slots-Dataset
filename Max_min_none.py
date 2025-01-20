import numpy as np
import copy
def Max_min_none(L):
    # x = L*2
    # y=L
    # x = L
    x = L.copy()

    Max = max(x[:,0])
    Min = min(x[:,0])
    Mean = np.mean(x[:,0])
    x[:,0] = 1.2*(x[:,0]-Mean)/(Max-Min)
    Max = max(x[:,1])
    Min = min(x[:,1])
    Mean = np.mean(x[:,1])
    x[:,1] = (x[:,1]-Mean)/(Max-Min)
    return x