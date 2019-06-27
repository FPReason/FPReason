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

def reasoning_system(fp1, fp2):
    delta = get_delta(fp1, fp2)
    if is_correlation(delta):
        return
    elif is_atomic(delta):
        return
    else:
        human_action()
        return

def get_delta(fp1, fp2):
    delta = {}
    for feature in fingerprint_change_fezoature_list:
        if fp1[feature] != fp2[feature]:
            delta[feature] = [fp1[feature], fp2[feature]]
    return delta

def is_correlation(delta):
    """
    All the exsiting correlation interfaces.
    """
    return False

def is_atomic(delta):
    """
    find out if it is atomic change.
    """
    if len(delta.keys()) > 1:
        return False
    else:
        atomic_feature = list(delta)[0]
        if atomic_feature == 'browserversion':
            return is_browser_update(delta)
        elif atomic_feature == 'timezone':
            return is_timezone_change(delta)
        elif atomic_feature == 'label':
            return is_private_mode(delta)
        elif atomic_feature == 'resolution':
            return is_zoom_in_out(delta)
        elif atomic_feature == 'language':
            return is_language_change(delta)
        elif atomic_feature == 'cookie':
            return is_cookie_enabled(delta)
        elif atomic_feature == 'localstorage':
            return is_local_storage(delta)
        elif atomic_feature == 'audio':
            return is_audio_change(delta)
        elif atomic_feature == 'fp2_colordepth':
            return is_colordepth_change(delta)
        elif atomic_feature == 'encoding':
            return is_encoding_change(delta)
        elif atomic_feature == 'jsFonts':
            return is_fonts_change(delta)
        elif atomic_feature == 'plugins':
            return is_plugins_change(delta)
        return False

def human_action(delta):
    """
    Human action interface.
    """
    print('human action')

def is_browser_update(delta):
    return True if delta['browserversion'][1] > delta['browserversion'][0] else False

def is_timezone_change(delta):
    return True if delta['timezone'][0] != delta['timezone'][1] else False

def is_private_mode(delta):
    return True if delta['label'][0] != delta['label'][1] else False

def is_zoom_in_out(delta):
    return True if delta['resolution'][0] != delta['resolution'][1] else False

def is_language_change(delta):
    return True if delta['language'][0] != delta['language'][1] else False

def is_cookie_enabled(delta):
    return True if delta['timezone'][0] != delta['timezone'][1] else False

def is_local_storage(delta):
    return True if delta['localstorage'][0] != delta['localstorage'][1] else False

def is_audio_change(delta):
    return True if delta['audio'][0] != delta['audio'][1] else False

def is_colordepth_change(delta):
    return True if delta['fp2_colordepth'][0] != delta['fp2_colordepth'][1] else False

def is_encoding_change(delta):
    return True if delta['encoding'][0] != delta['encoding'][1] else False

def is_fonts_change(delta):
    """
    Detailed fonts change. Different fonts change means different software update.
    """
    return False

def is_plugins_change(delta):
    """
    Detailed plugins change. Different plugins change means different software update.
    """
    return False

def main():
    db_origin = Database('origin')
    df_origin = db_origin.load_data(table_name='origin')
    fp1 = fp2 = df_origin[0]
    reasoning_system(fp1, fp2)

if __name__ == "__main__":
    main()

