import MySQLdb
import pandas
from database import Database
from feature_lists import *
import logging
import hashlib
from tqdm import *
import numpy as np
import csv
import time
from pathlib import Path
import pickle
import sys

def fonts_analysis():
    """
    analyse the top ranking fonts change.
    """
    csv.field_size_limit(sys.maxsize)
    with open("Delta_label.csv", 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        delta_list = list(reader)
    fonts_result = {}
    for item in tqdm(delta_list[0]):
        delta = list(item.split('!'))[1:]
        delta_features = delta[::3]
        if 'jsFonts' in delta_features:
            fonts_before = delta[delta.index('jsFonts') + 1]
            fonts_after = delta[delta.index('jsFonts') + 2]
            fonts_before_list = list(fonts_before.split(' '))
            fonts_after_list = list(fonts_after.split(' '))
            fonts_before_list,fonts_after_list = [i for i in fonts_before_list if i not in fonts_after_list],[j for j in fonts_after_list if j not in fonts_before_list]
            fonts_before_string = ' '.join(fonts_before_list)
            fonts_after_string = ' '.join(fonts_after_list)
            fonts_delta = fonts_before_string + '->' + fonts_after_string
            if fonts_delta in fonts_result:
                fonts_result[fonts_delta] += 1
            else:
                fonts_result[fonts_delta] = 1
    sorted_fonts = sorted(fonts_result.items(), key=operator.itemgetter(1), reverse=True)
    print('distinct fonts delta count: ' + str(len(sorted_fonts)))
    print(sorted_fonts[0])
    with open('Delta_fonts.txt', 'wb') as f:
        pickle.dump(sorted_fonts, f)
    #with open('Delta_fonts.txt', 'r') as f:
    #    delta_fonts = pickle.load(f)

def plugins_analysis():
    """
    ananlyse the top ranking plugins change.
    """
    csv.field_size_limit(sys.maxsize)
    with open("Delta_label.csv", 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        delta_list = list(reader)
    plugins_result = {}
    for item in tqdm(delta_list[0]):
        delta = list(item.split('!'))[1:]
        delta_features = delta[::3]
        if 'plugins' in delta_features:
            plugins_before = delta[delta.index('plugins') + 1]
            plugins_after = delta[delta.index('plugins') + 2]
            plugins_before_list = list(plugins_before.split('~'))
            plugins_after_list = list(plugins_after.split('~'))
            plugins_before_list,plugins_after_list = [i for i in plugins_before_list if i not in plugins_after_list],[j for j in plugins_after_list if j not in plugins_before_list]
            plugins_before_string = '~'.join(plugins_before_list)
            plugins_after_string = '~'.join(plugins_after_list)
            plugins_delta = plugins_before_string + '->' + plugins_after_string
            if plugins_delta in plugins_result:
                plugins_result[plugins_delta] += 1
            else:
                plugins_result[plugins_delta] = 1
    sorted_plugins = sorted(plugins_result.items(), key=operator.itemgetter(1), reverse=True)
    print('distinct plugins delta count: ' + str(len(sorted_plugins)))
    print(sorted_plugins[0])
    with open('Delta_plugins.txt', 'wb') as f:
        pickle.dump(sorted_plugins, f)

def correlation_analysis():
    """
    analyse the top ranking correlation deltas.
    """
    with open('Delta_rank.txt', 'rb') as f:
        delta_rank = pickle.load(f)

    for item in delta_rank:
        delta = list(item[0].split('!'))[1:]
        if len(delta) > 3:
            print(item)
            time.sleep(5)

def atomic_analysis():
    """
    analyse the top ranking atomic deltas.
    """
    with open('Delta_rank.txt', 'rb') as f:
        delta_rank = pickle.load(f)
    
    print(len(delta_rank))

    for item in delta_rank:
        delta = list(item[0].split('!'))[1:]
        if len(delta) == 3:
            print(item)
            time.sleep(5)

def main():
    #fonts_analysis()
    #plugins_analysis()
    #correlation_analysis()
    atomic_analysis()

if __name__ == "__main__":
    main()


