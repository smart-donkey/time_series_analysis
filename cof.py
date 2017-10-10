import numpy as np
import csv
import os
# import pandas


def get_data(d):
    file_list = []
    for f in  os.listdir(d):
        file_list.append(f)

    da = dict()
    for f in file_list:
        file_name = os.path.join(d, f)
        sd = read_file(file_name)
        da[f] = sd[1:]

    return da


def read_file(file_name):
    """
    read one data file
    :param file_name:
    :return:
    """
    sd = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for l in reader:
            sd.append(l[0])
    return sd


if __name__ == '__main__':
    da = get_data('st')
    keys = list(da.keys())
    a_d = []
    ind_2_keys = {i : k for i, k in enumerate(keys)}
    print(ind_2_keys)

    for k in keys:
        converted_d = np.asarray(da[k], dtype=np.float32)
        if len(a_d) == 0:
            a_d = converted_d[:, np.newaxis]
        else:
            a_d = np.concatenate((a_d, converted_d[:, np.newaxis]) , axis=1)


    # print()
    cof_m = np.corrcoef(a_d.T)
    print(cof_m)
    max_id = np.argmin(cof_m, axis=1)
    print(max_id)
    for id in max_id:
        print(ind_2_keys[id])

