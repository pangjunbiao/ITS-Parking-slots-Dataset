import copy

import numpy as np
from matplotlib import pyplot as plt
import math
from scipy.optimize import linear_sum_assignment
import gps_distance_google
import wrtxt
import wrtxt as wt
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


'''
@Date:  2020/2/23
@Author:ZhuJunHui
@Brief: Hungarian Algorithm using Python and NumPy
'''
import numpy as np
import collections
import time


class Hungarian():
    """
    """

    def __init__(self, input_matrix=None, is_profit_matrix=False):
        """
        输入为一个二维嵌套列表
        is_profit_matrix=False代表输入是消费矩阵（需要使消费最小化），反之则为利益矩阵（需要使利益最大化）
        """
        if input_matrix is not None:
            # 保存输入
            my_matrix = np.array(input_matrix)
            self._input_matrix = np.array(input_matrix)
            self._maxColumn = my_matrix.shape[1]
            self._maxRow = my_matrix.shape[0]

            # 本算法必须作用于方阵，如果不为方阵则填充0变为方阵
            matrix_size = max(self._maxColumn, self._maxRow)
            pad_columns = matrix_size - self._maxRow
            pad_rows = matrix_size - self._maxColumn
            my_matrix = np.pad(my_matrix, ((0, pad_columns), (0, pad_rows)), 'constant', constant_values=(0))

            # 如果需要，则转化为消费矩阵
            if is_profit_matrix:
                my_matrix = self.make_cost_matrix(my_matrix)

            self._cost_matrix = my_matrix
            self._size = len(my_matrix)
            self._shape = my_matrix.shape

            # 存放算法结果
            self._results = []
            self._totalPotential = 0
        else:
            self._cost_matrix = None

    def make_cost_matrix(self, profit_matrix):
        '''利益矩阵转化为消费矩阵，输出为numpy矩阵'''
        # 消费矩阵 = 利益矩阵最大值组成的矩阵 - 利益矩阵
        matrix_shape = profit_matrix.shape
        offset_matrix = np.ones(matrix_shape, dtype=int) * profit_matrix.max()
        cost_matrix = offset_matrix - profit_matrix
        return cost_matrix

    def get_results(self):
        """获取算法结果"""
        return self._results

    def calculate(self):
        """
        实施匈牙利算法的函数
        """
        result_matrix = self._cost_matrix.copy()

        # 步骤 1: 矩阵每一行减去本行的最小值
        for index, row in enumerate(result_matrix):
            result_matrix[index] -= row.min()

        # 步骤 2: 矩阵每一列减去本行的最小值
        for index, column in enumerate(result_matrix.T):
            result_matrix[:, index] -= column.min()
        # print('步骤2结果 ',result_matrix)
        # 步骤 3： 使用最少数量的划线覆盖矩阵中所有的0元素
        # 如果划线总数不等于矩阵的维度需要进行矩阵调整并重复循环此步骤
        total_covered = 0
        while total_covered < self._size:
            time.sleep(1)
            # print("---------------------------------------")
            # print('total_covered: ',total_covered)
            # print('result_matrix:',result_matrix)
            # 使用最少数量的划线覆盖矩阵中所有的0元素同时记录划线数量
            cover_zeros = CoverZeros(result_matrix)
            single_zero_pos_list = cover_zeros.calculate()
            covered_rows = cover_zeros.get_covered_rows()
            covered_columns = cover_zeros.get_covered_columns()
            total_covered = len(covered_rows) + len(covered_columns)

            # 如果划线总数不等于矩阵的维度需要进行矩阵调整（需要使用未覆盖处的最小元素）
            if total_covered < self._size:
                result_matrix = self._adjust_matrix_by_min_uncovered_num(result_matrix, covered_rows, covered_columns)
        # 元组形式结果对存放到列表
        self._results = single_zero_pos_list
        # 计算总期望结果
        value = 0
        for row, column in single_zero_pos_list:
            value += self._input_matrix[row, column]
        self._totalPotential = value

    def get_total_potential(self):
        return self._totalPotential

    def _adjust_matrix_by_min_uncovered_num(self, result_matrix, covered_rows, covered_columns):
        """计算未被覆盖元素中的最小值（m）,未被覆盖元素减去最小值m,行列划线交叉处加上最小值m"""
        adjusted_matrix = result_matrix
        # 计算未被覆盖元素中的最小值（m）
        elements = []
        for row_index, row in enumerate(result_matrix):
            if row_index not in covered_rows:
                for index, element in enumerate(row):
                    if index not in covered_columns:
                        elements.append(element)
        min_uncovered_num = min(elements)
        # print('min_uncovered_num:',min_uncovered_num)
        # 未被覆盖元素减去最小值m
        for row_index, row in enumerate(result_matrix):
            if row_index not in covered_rows:
                for index, element in enumerate(row):
                    if index not in covered_columns:
                        adjusted_matrix[row_index, index] -= min_uncovered_num
        # print('未被覆盖元素减去最小值m',adjusted_matrix)

        # 行列划线交叉处加上最小值m
        for row_ in covered_rows:
            for col_ in covered_columns:
                # print((row_,col_))
                adjusted_matrix[row_, col_] += min_uncovered_num
        # print('行列划线交叉处加上最小值m',adjusted_matrix)

        return adjusted_matrix


class CoverZeros():
    """
    使用最少数量的划线覆盖矩阵中的所有零
    输入为numpy方阵
    """

    def __init__(self, matrix):
        # 找到矩阵中零的位置（输出为同维度二值矩阵，0位置为true，非0位置为false）
        self._zero_locations = (matrix == 0)
        self._zero_locations_copy = self._zero_locations.copy()
        self._shape = matrix.shape

        # 存储划线盖住的行和列
        self._covered_rows = []
        self._covered_columns = []

    def get_covered_rows(self):
        """返回覆盖行索引列表"""
        return self._covered_rows

    def get_covered_columns(self):
        """返回覆盖列索引列表"""
        return self._covered_columns

    def row_scan(self, marked_zeros):
        '''扫描矩阵每一行，找到含0元素最少的行，对任意0元素标记（独立零元素），划去标记0元素（独立零元素）所在行和列存在的0元素'''
        min_row_zero_nums = [9999999, -1]
        for index, row in enumerate(self._zero_locations_copy):  # index为行号
            row_zero_nums = collections.Counter(row)[True]
            if row_zero_nums < min_row_zero_nums[0] and row_zero_nums != 0:
                # 找最少0元素的行
                min_row_zero_nums = [row_zero_nums, index]
        # 最少0元素的行
        row_min = self._zero_locations_copy[min_row_zero_nums[1], :]
        # 找到此行中任意一个0元素的索引位置即可
        row_indices, = np.where(row_min)
        # 标记该0元素
        # print('row_min',row_min)
        marked_zeros.append((min_row_zero_nums[1], row_indices[0]))
        # 划去该0元素所在行和列存在的0元素
        # 因为被覆盖，所以把二值矩阵_zero_locations中相应的行列全部置为false
        self._zero_locations_copy[:, row_indices[0]] = np.array([False for _ in range(self._shape[0])])
        self._zero_locations_copy[min_row_zero_nums[1], :] = np.array([False for _ in range(self._shape[0])])

    def calculate(self):
        '''进行计算'''
        # 储存勾选的行和列
        ticked_row = []
        ticked_col = []
        marked_zeros = []
        # 1、试指派并标记独立零元素
        while True:
            # print('_zero_locations_copy',self._zero_locations_copy)
            # 循环直到所有零元素被处理（_zero_locations中没有true）
            if True not in self._zero_locations_copy:
                break
            self.row_scan(marked_zeros)

        # 2、无被标记0（独立零元素）的行打勾
        independent_zero_row_list = [pos[0] for pos in marked_zeros]
        ticked_row = list(set(range(self._shape[0])) - set(independent_zero_row_list))
        # 重复3,4直到不能再打勾
        TICK_FLAG = True
        while TICK_FLAG:
            # print('ticked_row:',ticked_row,'   ticked_col:',ticked_col)
            TICK_FLAG = False
            # 3、对打勾的行中所含0元素的列打勾
            for row in ticked_row:
                # 找到此行
                row_array = self._zero_locations[row, :]
                # 找到此行中0元素的索引位置
                for i in range(len(row_array)):
                    if row_array[i] == True and i not in ticked_col:
                        ticked_col.append(i)
                        TICK_FLAG = True

            # 4、对打勾的列中所含独立0元素的行打勾
            for row, col in marked_zeros:
                if col in ticked_col and row not in ticked_row:
                    ticked_row.append(row)
                    FLAG = True
        # 对打勾的列和没有打勾的行画画线
        self._covered_rows = list(set(range(self._shape[0])) - set(ticked_row))
        self._covered_columns = ticked_col

        return marked_zeros
def makematrix(a,b):
    a_len = len(a)
    b_len = len(b)
    matrix_a = np.zeros((a_len,b_len))
    for i in range(a_len):
        for j in range(b_len):
            distance = a[i][0]-b[j][0]+a[i][1]-b[j][1]
            matrix_a[i][j] = abs(distance)
    return matrix_a

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

if __name__ == '__main__':
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
    # lon = copy.copy(R[:, 0])
    # lat = copy.copy(R[:, 1])
    # min_lon = np.min(lon)
    # min_lat = np.min(lat)
    # len_P = len(P)
    # len_R = len(R)
    # P = initial(P)  # 输入的偏移park
    # R = initial(R)
    # P = tftmatrox(P, math.pi * -15 / 180, [0, 0])
    # P = P + [0.002, -0.0001]
    # P += [min_lon,min_lat]
    # R += [min_lon,min_lat]
    # cost_matrix = makematrix(R, P)
    # row_ind, col_ind = linear_sum_assignment(cost_matrix)
    #
    # y = []
    # for i in row_ind:
    #     y.append(R[i])
    # y = np.array(y)
    # plt.scatter(R[:, 0], R[:, 1], label="predicted parking spaces", c="r")
    # plt.scatter(P[:, 0], P[:, 1], label="collected　parking　spaces", c="b")
    # plt.scatter(y[:, 0], y[:, 1], c="k", label="matched parking spaces")
    # plt.show()
    # wrtxt.writetxtred(R,"xd.mif")
    # wrtxt.writetxtblue(P,"xd.mif")
    # wrtxt.writetxtblack(y,"xd.mif")
    #
    true_list = []
    curse_list = [0,4,9,12,13,17,21,22,25,27,28]#曲线
    precision = 0
    R_list = np.load("road.npy", allow_pickle=True)
    P_list = np.load("park.npy", allow_pickle=True)
    best_park_list = np.load("gt.npy", allow_pickle=True)
    np.random.seed(999)
    num = 0
    long_len = 0
    n=0
    for index in range(51):
    # for index in curse_list:
        if index in curse_list:
            continue
        n+=1
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
        a = np.random.random((len_P, 1)) / 5000  # 0.0002 and  0.0005
        b = np.random.random((len_P, 1)) / 5000
        b = np.zeros((len_P, 1))
        c = np.c_[a, b]
        P = P + a
        cost_matrix = makematrix(R, P)
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        y = []
        for i in row_ind:
         y.append(R[i])
        y = np.array(y)
        long_len+=len_P
        if len(y) == len(best_park):
         for item in range(len(best_park)):
             if y[item] in best_park:
                 num+=1
         a = np.mean(np.abs(y - best_park))
        else:
         print(index)
         break
        precision += a
        print(index)

    precision = gps_distance_google.do(precision /n)
    num_av = num/long_len
    print('定位准确度',precision)
    print("召回率：",num_av)

