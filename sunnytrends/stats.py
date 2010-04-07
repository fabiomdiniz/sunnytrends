# -*- coding: utf-8 -*-

from deps.statlib.stats import *

def list_difference(list1, list2):
    return list(set(list1)-set(list2))

def make_report(func, data_matrix):
    report = {'values':[], 'first':[], 'second':[]}    
    next_data = 1    
    for data_list_1 in data_matrix[:-1]:
        for i in range(len(data_matrix)-next_data):
            report['values'].append(func([data for data in data_list_1], \
                                               [data for data in data_matrix[next_data + i]])[0])
            report['first'].append(data_list_1[0].__class__.__name__)
            report['second'].append(data_matrix[next_data + i][0].__class__.__name__)
        next_data += 1
    return report
    
def make_sunny_report(func, data_matrix, sunny_index, keys):
    report = {'values':[], 'data':[]}
    for data_list in data_matrix:
        if data_matrix.index(data_list) != sunny_index:
            report['values'].append(func([data for data in data_list], \
                                         [data for data in data_matrix[sunny_index]])[0])
            report['data'].append(keys[data_matrix.index(data_list)])
    return report