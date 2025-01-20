def out_cross(temp_name_r,link_type,name_link,link_dict):
    # print("十字路口路：",temp_name_r)
    crossroad_list = []
    lat_test_list = []
    lon_test_list = []
    for i in range(len(link_type[temp_name_r])):
        if link_type[temp_name_r][i] == '4':
            crossroad_list.append(i)
        print(crossroad_list)
    k = 0

    for j in crossroad_list:
        if j == crossroad_list[-1]:
            if k != j:
                temp_link1 = name_link[temp_name_r][k:j]
                for temp in temp_link1:
                # temp_lat_1, temp_lon_1 = interk(one_[:, 1], one_[:, 0])
                    temp_lat_1, temp_lon_1 = interk(np.array(link_dict[temp])[:, 1], np.array(link_dict[temp])[:, 0])
                    lat_test_list.extend(temp_lat_1)
                    lon_test_list.extend(temp_lon_1)
            temp_link2 = np.array(name_link[temp_name_r][j + 1:])
            if np.size(temp_link2) != 0:
                for temp in temp_link2:
                    temp_lat_2, temp_lon_2 = interk(np.array(link_dict[temp])[:, 1], np.array(link_dict[temp])[:, 0])
                    lon_test_list.extend(temp_lon_2)
                    lat_test_list.extend(temp_lat_2)
        else:
            if k != j :
                temp_link = name_link[temp_name_r][k:j]
                for temp in temp_link:
                    temp_lat_1, temp_lon_1 = interk(np.array(link_dict[temp])[:, 1], np.array(link_dict[temp])[:, 0])
                    lon_test_list.extend(temp_lon_1)
                    lat_test_list.extend(temp_lat_1)
        k = j+1
    x_temp = np.array(lon_test_list)
    y_temp = np.array(lat_test_list)
    max_lon = max(x_temp)
    min_lon = min(x_temp)
    max_lat = max(y_temp)
    min_lat = min(y_temp)
    err_lat = max_lat - min_lat
    err_lon = max_lon-min_lon
    lon_lat_list =[]
    if err_lat >= err_lon:
        lon_lat_t = np.c_[y_temp,x_temp]
        numsort = np.argsort(lon_lat_t[:,0],axis=0)
        print(numsort)
        for tempnum in numsort:
            lon_lat_list.append(lon_lat_t[tempnum])
        lon_lat_arr = np.array(lon_lat_list)
        x = lon_lat_arr[:,1]
        y = lon_lat_arr[:,0]
    if err_lat < err_lon:
        lon_lat_t = np.c_[x_temp, y_temp]
        numsort = np.argsort(lon_lat_t[:, 0], axis=0)
        print(numsort)
        for tempnum in numsort:
            lon_lat_list.append(lon_lat_t[tempnum])
        lon_lat_arr = np.array(lon_lat_list)
        x = lon_lat_arr[:, 0]
        y = lon_lat_arr[:, 1]
    return x,y