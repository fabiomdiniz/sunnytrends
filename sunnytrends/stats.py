# -*- coding: utf-8 -*-

from deps.statlib.stats import *

def make_report(func, data_matrix):
    report = {'values':[], 'first':[], 'second':[]}    
    next_data = 1    
    for data_list_1 in data_matrix[:-1]:
        for i in range(len(data_matrix)-next_data):
            report['values'].append(func([data.value for data in data_list_1], \
                                               [data.value for data in data_matrix[next_data + i]])[0])
            report['first'].append(data_list_1[0].__class__.__name__)
            report['second'].append(data_matrix[next_data + i][0].__class__.__name__)
        next_data += 1
    return report
