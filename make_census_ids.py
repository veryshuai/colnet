# This python script makes ids just like those used at the census

import pandas as pd

if __name__ == "__main__":
    """loads network data, creates census ids,
        converts to numeric values, and saves"""

    # LOAD DATA
    dat    = pd.read_csv('network_data.csv',delimiter='|',quotechar='"')
    dat.to_pickle('dat.pandas')
    dat     = pd.read_pickle('dat.pandas')
    
    #CREATE FIRM ID
    dat['STR_ID'] = dat['COD_PAI3'].str.strip().str[:3]\
            + dat['CIU_PDES'].str.strip().str[:3]\
            + dat['RAZN_IMP'].str.strip().str[:3]# + dat['DIR_PDES'].str.strip().str[:2]
    dat['STR_ID'] = dat['STR_ID'].str.upper()
    
    #CREATE YEAR
    dat['YEAR'] = dat['FECH_PR3'].apply(lambda x: x / 100)

    #YEAR FILTER
    dat = dat[dat['YEAR'] == 2009]
    
    #REPLACE STRINGS WITH NUMBERS - IMPORTER
    grouped = dat.groupby('STR_ID')['COD_PAI3'].first() # unique row for each firm
    grouped = pd.DataFrame(grouped).reset_index().reset_index() # create unique numerical index for each firm
    dat     = pd.merge(dat, grouped, on='STR_ID') # merge into original data
    
    #REPLACE STRINGS WITH NUMBERS - EXPORTER
    grouped = dat.groupby('NIT3')['COD_PAI3_x'].first() # unique row for each firm
    grouped = pd.DataFrame(grouped).reset_index().reset_index() # create unique numerical index for each firm
    dat     = pd.merge(dat, grouped, on='NIT3') # merge into original data

    #CREATE NUM ID TRANSLATION LISTS
    dat[['STR_ID', 'index_x']].groupby('index_x').first().to_csv('importer_id.csv')
    dat[['NIT3', 'index_y']].groupby('index_y').first().to_csv('exporter_id.csv')
    
    #CREATE REDUCED DATA
    red_dat         = dat[['index_y','index_x','YEAR','POS_ARA3','FOB_DOL3']]
    red_dat.columns = ['EXP_ID','IMP_ID','YEAR','POS_ARA3','FOB_DOL3']

    #OUTPUT TO CSV
    red_dat.to_csv('graph_trans.csv')

