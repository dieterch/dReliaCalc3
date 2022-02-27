import arrow; print(arrow.now('Europe/Vienna').format('DD.MM.YYYY - HH:mm'))

import dmyplant2
import pandas as pd
import numpy as np
from tabulate import tabulate
from pprint import pprint as pp
import matplotlib.pyplot as plt

from dmyplant2 import cred
mp = dmyplant2.MyPlant(3600)

dval = dmyplant2.Validation.load_def_csv("input2.csv")
vl = dmyplant2.Validation(mp,dval, cui_log=True) 

dat3 = {
    102: ['Power current', 'kW'],
    217: ['Pressure crankcase', 'mbar'],
    16546: ['Oil difference pressure', 'bar'],
    161: ['Operating hours engine', 'nan']
}

dset3 = [
            {'col':['Power current'], 'ylim':(0,5000)},
            {'col': ['Pressure crankcase'],'ylim': [-80, 120]},
            {'col':['Oil difference pressure'], 'ylim':(0,2)},
            {'col':['Oph parts'], 'ylim':(0,10000)}
        ]

psize = (12,8)

def runplots(n0, n1, dat, plotset):
    for ee in vl.engines[n0:n1]:
        lldf = mp.hist_data( 
            ee.id, 
            itemIds= dat, 
            p_from=arrow.get(ee.val_start).to('Europe/Vienna'), 
            p_to=arrow.now('Europe/Vienna'), 
            timeCycle=600)
        #print(lldf)
        lldf['Oph parts'] = lldf['Operating hours engine'] - ee.oph_start
        dmyplant2.dbokeh_chart(lldf, plotset, title = ee, figsize=psize, notebook=False)

runplots(0,1, dat3, dset3)
plt.show()
