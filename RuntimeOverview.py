import warnings
import matplotlib.pyplot as plt
from pprint import pprint as pp
from tabulate import tabulate
import numpy as np
import pandas as pd
import dmyplant2
import arrow
print(arrow.now('Europe/Vienna').format('DD.MM.YYYY - HH:mm'))

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

dmyplant2.cred()
mp = dmyplant2.MyPlant(600)
dval = dmyplant2.Validation.load_def_csv("input2.csv")
vl = dmyplant2.Validation(mp, dval, cui_log=True)


def runplot(n, dat, plotset):
    ee = vl.engines[n]
    lldf = ee.hist_data(
        # ee.id,
        itemIds=dat,
        p_from=arrow.get(ee.val_start).to('Europe/Vienna'),
        p_to=arrow.now('Europe/Vienna'),
        timeCycle=600)
    lldf['Oph parts'] = lldf.Count_OpHour - ee.oph_start
    dmyplant2.chart(lldf, plotset, title=ee, figsize=psize)

    # Lube Oil Consuption data
    dloc = ee.Validation_period_LOC()
    dmyplant2.chart(dloc, [
        {'col': ['OilConsumption', 'LOC'], 'ylim': (0, 0.8)},
        {'col': ['Pow'], 'ylim': (0, 8000)},
    ],
        title=ee,
        figsize=psize)


dat3 = {
    102: ['Power_PowerAct', 'kW'],
    217: ['Hyd_PressCrankCase', 'mbar'],
    16546: ['Hyd_PressOilDif', 'bar'],
    161: ['Count_OpHour', 'nan'],
    69: ['Hyd_PressCoolWat', 'bar'],
}

dset3 = [
    {'col': ['Power_PowerAct'], 'ylim':(0, 5000), 'color':'red'},
    {'col': ['Hyd_PressCrankCase'], 'ylim': [-80, 120]},
    {'col': ['Hyd_PressOilDif'], 'ylim':(0, 2)},
    {'col': ['Hyd_PressCoolWat'], 'ylim': [1, 3]},
    {'col': ['Oph parts'], 'ylim':(0, 10000)}
]

psize = (12, 8)

runplot(0, dat3, dset3)
plt.show()
