import numpy as np
import csv
import os
import pandas as pd


def get_data(d):
    file_list = []
    for f in  os.listdir(d):
        file_list.append(f)

    da = dict()
    ind_2_key = []
    key_2_ind = dict()
    for f in file_list:
        file_name = os.path.join(d, f)
        # print(file_name)
        sd = pd.read_csv(file_name)
        if len(sd) > 70:
            da[f] = sd.last_price
            np_ar = np.asarray(da[f], dtype=np.float32)
            if len(np_ar[np_ar == 0]) > 0:
                print('zero count: {}, file name: {}'.format(len(np_ar[np_ar == 0]), f))
            else:
                key_2_ind[f] = len(key_2_ind)
                ind_2_key.append(f)

    return da, key_2_ind, ind_2_key


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
            last_price = l[0]
            sd.append(last_price)
    return sd


def display_results(cof_m, ind_2_key, key_2_ind, q_index, top = 5):
    min_inds = np.argsort(cof_m, axis=1)
    print('source:', ind_2_key[q_index])
    print('target: ')
    for t in min_inds[q_index][: top]:
        print(ind_2_key[t], cof_m[q_index][t])



if __name__ == '__main__':
    da, key_2_ind, ind_2_key = get_data('st')
    keys = list(da.keys())
    a_d = []
    # ind_2_keys = {i : k for i, k in enumerate(keys)}
    # print(ind_2_keys)

    for k in ind_2_key:
        converted_d = np.asarray(da[k], dtype=np.float32)
        if len(a_d) == 0:
            a_d = converted_d[:, np.newaxis]
        else:
            a_d = np.concatenate((a_d, converted_d[:, np.newaxis]) , axis=1)

    # print(a_d.T[1, :])
    # print(np.diff(a_d.T,axis=1)/ a_d.T[:, :-1] )
    features = np.diff(a_d.T, axis=1)/ a_d.T[:, :-1]
    # print(a_d[a_d==0])
    # print(-np.diff(a_d.T[1,: ]))
    # print(features.shape)
    # print(features * 100)
    cof_m = np.corrcoef(features * 100)
    # print(cof_m[1])

    # print(np.sort(np.min(cof_m, axis=1)))
    # print(np.argsort(np.min(cof_m, axis=1)))

    # wanted_list = []
    with open('wanted_list.yaml') as f:
        import yaml
        wanted_list = yaml.load(f)

    indices = []
    keys = key_2_ind.keys()
    for w in wanted_list:
        find_k = None
        for k in keys:
            if k.find(w) >=0:
                # print(k)
                find_k = k
                break

        indices.append(key_2_ind[find_k])

    for s in indices:
        display_results(cof_m, ind_2_key, key_2_ind, s)


    # for s in np.argsort(np.min(cof_m, axis=1))[:20]:
    #     display_results(cof_m, ind_2_key, key_2_ind, s)

    # # print()
    #
    # print(cof_m)
    # min_id = np.argsort(cof_m, axis=1)
    # min_id = max_id[:, :5]
    # print(min_id[:, :10])
    # print(cof_m[:5][min_id])
    # for id in max_id:
    #     print(ind_2_keys[id])

