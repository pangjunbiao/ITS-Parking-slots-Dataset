import xlrd
import xlwt
import matplotlib.pyplot as plt
import strfloat
import numpy as np
def read_excel():
    # 打开文件
    workBook = xlrd.open_workbook('nanxinhua.xlsx')

    # 1.获取sheet的名字
    # 1.1 获取所有sheet的名字(list类型)
    allSheetNames = workBook.sheet_names()
    # print(allSheetNames)

    # 1.2 按索引号获取sheet的名字（string类型）
    sheet1Name = workBook.sheet_names()[0]
    # print(sheet1Name)

    # 2. 获取sheet内容
    ## 2.1 法1：按索引号获取sheet内容
    sheet1_content1 = workBook.sheet_by_index(0)# sheet索引从0开始
    ## 2.2 法2：按sheet名字获取sheet内容
    sheet1_content2 = workBook.sheet_by_name('Sheet1')

    # 3. sheet的名称，行数，列数
    # print(sheet1_content1.name,sheet1_content1.nrows,sheet1_content1.ncols)

    # 4. 获取整行和整列的值（数组）
    #cols_name为道路名字
    #cols_lon为道路经度
    #cols_lat为道路纬度
    # rows = sheet1_content1.row_values()# 获取第四行内容
    # cols_name = sheet1_content1.col_values(0)# 获取第三列内容
    cols_lon = sheet1_content1.col_values(0)# 获取第三列内容
    cols_lat = sheet1_content1.col_values(1)# 获取第三列内容
    #去除标题行
    # cols_name = cols_name[1:]
    # cols_lon = cols_lon[1:]
    # cols_lat = cols_lat[1:]
    return cols_lon,cols_lat

    # 5. 获取单元格内容(三种方式)
    # print(sheet1_content1.cell(1, 0).value)
    # print(sheet1_content1.cell_value(2, 2))
    # print(sheet1_content1.row(2)[2].value)

    # 6. 获取单元格内容的数据类型
    # Tips: python读取excel中单元格的内容返回的有5种类型 [0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error]
    # print(sheet1_content1.cell(1, 0).ctype)


if __name__ == '__main__':
    cols_lon,cols_lat=read_excel()
    # for temp in range(np.size(cols_lat)):
    cols_lon,cols_lat = strfloat.transform(cols_lon, cols_lat)

    plt.scatter(cols_lon,cols_lat)
    plt.show()
    print(cols_lat,cols_lon)
