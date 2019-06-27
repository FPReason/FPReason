import MySQLdb
import pandas
from database import Database
from feature_lists import *
from tqdm import *
import numpy as np
import csv
import time
import pickle
import sys

def is_same_fingerprint(pre_value, cur_value)
    """
    compare if it is the same fingerprint
    """
    for feature in fingerprint_change_feature_list:
        same_flag = 'same'
        if pre_value[feature] != cur_value[feature]:
            same_flag = 'diff'
        break
    if same_flag == 'same':
        return True
    else:
        return False

def apply_operation_set(pre_value, cur_value):
    """
    find different operations, an extensible function.
    """
    print()

def generate_delta_to_csv(df_origin):
    """
    generate the delta set and save in csv
    """
    result_list = []
    result_dict = {}
    df_group_browserid = df_origin.groupby('browserid')
    for key, cur_group in tqdm(df_group_browserid):
        pre_value = pd.Series() 
        for idx, row in cur_group.iterrows():
            if pre_value.empty:
                pre_value = row
                continue
            else:
                cur_value = row
                same_flag = 'same'
                temp_string = ''
                for feature in fingerprint_change_feature_list:
                    if pre_value[feature] != cur_value[feature]:
                        same_flag = 'diff'
                        temp_string = temp_string + '!' + feature + '!' + pre_value[feature] + '!' + cur_value[feature]
                if temp_string not in result_list:
                    result_list.append(temp_string)
                if temp_string not in result_dict:
                    result_dict[temp_string] = 1
                else:
                    result_dict[temp_string] += 1
    with open('Delta.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(result_list)
    sorted_delta = sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True)
    with open('Delta_rank.txt', 'wb') as f:
        pickle.dump(sorted_delta, f)

def analyse_delta():
    """
    analyse all delta and get the operations
    """
    csv.field_size_limit(sys.maxsize)
    with open("Delta.csv", 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        delta_list = list(reader)

    print('The count of delta is {}'.format(len(delta_list[0])))

    browser_update = 0
    os_update = 0
    timezone_change = 0
    private_mode = 0
    zoom_in_out = 0
    language_change = 0
    cookie_enabled = 0
    local_storage = 0
    audio_change = 0
    color_depth = 0
    canvas_test = 0
    resolution_change = 0
    encoding_change = 0
    fonts_list = []
    plugins_list = []
    correlation_list = []

    for item in tqdm(delta_list[0]):
        delta = list(item.split('!'))[1:]
        delta_features = delta[::3]
        if len(delta_features) == 1:
            if delta_features[0] == 'browserversion':
                browser_update += 1
            elif delta_features[0] == 'timezone':
                timezone_change += 1
            elif delta_features[0] == 'label':
                private_mode += 1
            elif delta_features[0] == 'resolution':
                resolution_change += 1
            elif delta_features[0] == 'language':
                language_change += 1
            elif delta_features[0] == 'cookie':
                cookie_enabled += 1
            elif delta_features[0] == 'localstorage':
                local_storage += 1
            elif delta_features[0] == 'audio':
                audio_change += 1
            elif delta_features[0] == 'fp2_colordepth':
                color_depth += 1
            elif delta_features[0] == 'canvastest':
                canvas_test += 1
            elif delta_features[0] == 'fp2_pixelratio':
                zoom_in_out += 1
            elif delta_features[0] == 'encoding':
                encoding_change += 1
            elif delta_features[0] == 'osversion':
                os_update += 1
            elif delta_features[0] == 'jsFonts':
                if [delta[1], delta[2]] not in fonts_list:
                    fonts_list.append([delta[1], delta[2]])
            elif delta_features[0] == 'plugins':
                if [delta[1], delta[2]] not in plugins_list:
                    plugins_list.append([delta[1], delta[2]])
            else:
                print(delta_features[0])
        else:
            if item not in correlation_list:
                correlation_list.append(item)
    print(len(correlation_list))

    with open('Delta_correlation.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(correlation_list)
    
    with open('Delta_result.txt', 'w') as myfile:
        myfile.write('browserversion change: ' + str(browser_update) + ' timezone change: ' + str(timezone_change) 
                    +' label change: ' + str(private_mode) + ' resolution change: ' + str(resolution_change)
                    +' language change: ' + str(language_change) + ' cookie enabled: ' + str(cookie_enabled)
                    +' local storage: ' + str(local_storage) + ' audio change: ' + str(audio_change) 
                    +' fp2_colordepth: ' + str(color_depth) + ' canvas test: ' + str(canvas_test) + ' zoom_in_out: ' + str(fp2_pixelratio)
                    +' os update: ' + str(os_update) + ' encoding_change: ' + str(encoding_change) 
                    + ' jsFonts: ' + str(len(fonts_list)) + ' plugins: ' + str(len(plugins_list)))

def analyse_correlation():
    """
    anaylse all the correlations.
    """
    csv.field_size_limit(sys.maxsize)
    with open("Delta_correlation.csv", 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        delta_list = list(reader)
    correlation_frequency = {}
    for delta in tqdm(delta_list[0]):
        if delta not in correlation_frequency:
            correlation_frequency[delta] = 1
        else:
            correlation_frequency[delta] += 1
    sorted_correlation = sorted(correlation_frequency.items(), key=operator.itemgetter(1), reverse=True)

def main():
    db_origin = Database('origin')
    df_origin = db_origin.load_data(table_name='origin')
    generate_delta_to_csv(df_origin)
    #analyse_delta()
    #analyse_correlation()

if __name__ == "__main__":
    main()
