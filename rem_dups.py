# This script removes duplicate transactions from graph_trans.csv
# and sums fob values

import pandas as pd

def error_proof_convert(x):
    try:
        arg = sum([float(k) for k in list(x)])
        return arg
    except:
        print 'WARNING: Unreadable line in graph_trans.csv'
        return 0

def main():
    dat = pd.read_csv('graph_trans.csv')
    val = dat.reset_index().groupby(['EXP_ID','IMP_ID'])['FOB_DOL3'].apply(error_proof_convert)
    dat = dat.drop_duplicates(['EXP_ID','IMP_ID'])
    dat = dat.reset_index()[['EXP_ID','IMP_ID','POS_ARA3','FOB_DOL3']].set_index(['EXP_ID','IMP_ID'])
    dat['FOB_DOL3'] = val
    dat.reset_index().set_index('EXP_ID')
    dat.to_csv('graph.csv')

main()
