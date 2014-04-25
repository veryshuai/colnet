# This python script makes ids just like those used at the census

import pandas as pd

if __name__ == "__main__":
    """loads network data, creates census ids,
        converts to numeric values, and saves"""

    # LOAD DATA
    #dat    = pd.read_csv('network_data.csv', delimiter='|', quotechar='"', error_bad_lines=False, encoding='iso-8859-1')
    #dat.to_pickle('network_data.pickle')
    dat = pd.read_pickle('network_data.pickle')

    #CREATE FIRM ID
    dat['STR_ID'] = dat['imp_name'].str.strip().str[:7]\
            + dat['dest_alf'].str.strip().str[:3]
            #+ dat['imp_city'].str.strip().str[:3]\
            #+ dat['imp_address'].str.strip().str[:2]
    dat['STR_ID'] = dat['STR_ID'].str.upper()

    #DROP NO NAMES, AND NON-INFORMATIVE NAMES
    dat = dat[dat['imp_name'] != '']
    dat = dat[dat['imp_name'] != 'TO ORDER']
    dat = dat[dat['imp_name'].str.strip() != 'TO THE ORDER OF']
    dat = dat[dat['imp_name'].str.strip() != 'TO THE ORDER']
    dat = dat[dat['imp_name'] != 'A LA ORDEN']

    #CREATE YEAR
    dat['YEAR'] = dat['yr_month'].apply(lambda x: int(x / 100))

    #YEAR FILTER
    dat = dat[dat['YEAR'] == 2009]
    
    #REPLACE STRINGS WITH NUMBERS - IMPORTER
    grouped = dat.groupby('STR_ID')['dest_alf'].first() # unique row for each firm
    grouped = pd.DataFrame(grouped).reset_index().reset_index() # create unique numerical index for each firm
    dat     = pd.merge(dat, grouped, on='STR_ID') # merge into original data

    #REPLACE STRINGS WITH NUMBERS - EXPORTER
    #grouped = dat.groupby('exp_id')['dest_code'].first() # unique row for each firm
    grouped = dat.drop_duplicates(cols='exp_id') # unique row for each firm
    grouped = grouped.reset_index().drop('level_0', 1).reset_index() # create unique numerical index for each firm
    grouped['index'] = grouped['level_0'] #kludge to make indexes match
    grouped = grouped[['index', 'exp_id']]
    dat     = pd.merge(dat, grouped, on='exp_id', suffixes=('_x','_y') )# merge into original data

    #CREATE NUM ID TRANSLATION LISTS
    dat[['STR_ID', 'index_x']].groupby('index_x').first().to_csv('importer_id.csv')
    dat[['exp_id', 'index_y']].groupby('index_y').first().to_csv('exporter_id.csv')

    #CREATE REDUCED DATA
    red_dat         = dat[['index_y','index_x','YEAR','hs10','x_fob','dest_alf_x','STR_ID', 'exp_id', 'imp_name']]
    red_dat.columns = ['EXP_ID','IMP_ID','YEAR','hs10','x_fob','dest_alf','imp_alf','exp_id_orig', 'imp_name']

    #OUTPUT TO CSV
    red_dat.to_csv('graph_trans.csv')

