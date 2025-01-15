# Supporting functions to manage configuration and data


## Data and config save functions

import config as cfg
import glob


def get_bin_log_id():
    ''' find exsisting file number'''
    files = glob.glob(f"{cfg.data_location}/*.bin")
    return len(files)
