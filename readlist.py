import xlrd
import xlwt
import numpy as np

def read_excel():
    # 打开文件
    workBook = xlrd.open_workbook('停车点数据.xlsx')

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
    cols_name = sheet1_content1.col_values(2)# 获取第三列内容
    start_cols_lon = sheet1_content1.col_values(1)# 获取第三列内容
    start_cols_lat = sheet1_content1.col_values(3)# 获取第三列内容
    last_cols_lon = sheet1_content1.col_values(2)# 获取第三列内容
    last_cols_lat = sheet1_content1.col_values(4)# 获取第三列内容
    #去除标题行
    cols_name = cols_name[1:]
    start_cols_lon = start_cols_lon[1:]
    start_cols_lat = start_cols_lat[1:]
    last_cols_lon = last_cols_lon[1:]
    last_cols_lat = last_cols_lat[1:]


    return cols_name,start_cols_lon,start_cols_lat,last_cols_lon,last_cols_lat

    # 5. 获取单元格内容(三种方式)
    # print(sheet1_content1.cell(1, 0).value)
    # print(sheet1_content1.cell_value(2, 2))
    # print(sheet1_content1.row(2)[2].value)

    # 6. 获取单元格内容的数据类型
    # Tips: python读取excel中单元格的内容返回的有5种类型 [0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error]
    # print(sheet1_content1.cell(1, 0).ctype)


if __name__ == '__main__':
    cols_name,start_lng,start_lat,last_lng,last_lat = read_excel()

    for index in range(5):
        if index == 0:
            filename = "gps" + "0"+"txt"
            with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                for temp in cols_name:
                    f.write('\"')
                    f.write(temp)
                    f.write('\"')
                    f.write(',')
                # f.write("I am now studying in NJTECH.\n")
        if index ==1:
            filename = "gps" + "1.txt"
            with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                for temp in range(len(start_lat)):
                    start_lng[temp] = str(start_lng[temp])
                    start_lat[temp] = str(start_lat[temp])
                    last_lng[temp] = str(last_lng[temp])
                    last_lat[temp] = str(last_lat[temp])
                    com = '['+"new BMap.Point"+'('+start_lng[temp]+','+start_lat[temp]+')'+','+"new BMap.Point"+'('+last_lng[temp]+','+last_lat[temp]+')'']'
                    f.write(com)
                    f.write(',')
        # if index == 2:
        #     filename = "gps" + "2"
        #     with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        #         for temp in range(len(last_lat)):
        #
        #             com =
        #             f.write(com)
        #             f.write(',')
        # if index == 3:
        #     filename = "gps" + "3"
        #     with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        #         for temp in last_lng:
        #             temp = str(temp)
        #             f.write(temp)
        #             f.write(',')
        # if index == 4:
        #     filename = "gps" + "4"
        #     with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        #         for temp in last_lat:
        #             temp = str(temp)
        #             f.write(temp)
        #             f.write(',')


