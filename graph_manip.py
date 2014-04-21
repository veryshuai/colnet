# This script processes a raw edgelist for plotting and manipulation in igraph

import pandas as pd
import numpy as np

#load data
dat = pd.read_csv('graph.csv',delimiter=',')
val = dat['FOB_DOL3']
dat = dat[['EXP_ID','IMP_ID']]

# make low values for nodes
dat['EXP_ID'] = pd.factorize(dat['EXP_ID'])[0]
dat['IMP_ID'] = pd.factorize(dat['IMP_ID'])[0]
# give exporters nad importers unique ids
dat['IMP_ID'] = dat['IMP_ID'] + dat['EXP_ID'].max() + 1
dat.set_index('EXP_ID').to_csv('igraph_small.csv')
val.to_csv('vals_small.csv')


