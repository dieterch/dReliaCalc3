import dmyplant2
import pandas as pd
import numpy as np
from pprint import pprint as pp
import matplotlib.pyplot as plt
import sys

df_desc = pd.read_hdf("./data/1184199_1.hdf", 'description')
df_data = pd.read_hdf("./data/1184199_1.hdf", 'data')

pp(df_desc)

dmyplant2.cred()  # Ask for credentials every month
mp = dmyplant2.MyPlant(7200)  # login to myplant and keep connection
dat = mp.load_dataitems_csv("DataItems_Request.csv")
e = dmyplant2.Engine_SN(mp, '1184199')  # create Engine Class Instance

# dfs = df[
#    (df['datetime'] > pd.to_datetime('2021-02-21 09:00')) &
#    (df['datetime'] < pd.to_datetime('2021-02-21 17:00'))
# ].copy()
dfs = df_data[:-1].copy()
dfs['diff'] = np.diff(df_data['PowerAct'])

#dfs['HZ'] = dfs['Various_Values_SpeedAct'] / 1500.0 * 50.0

print(f"Size of Dataframe {sys.getsizeof(df_data) / 1e6} MB")

dset = [{'col': ['Power_PowerAct'], 'ylim':(0, 5000)},
        {'col': ['Various_Values_SpeedAct'], 'ylim':(1350, 1550)},
        {'col': ['HZ'], 'ylim':(47.5, 51.5)},
        {'col': ['Various_Values_PressBoost'], 'ylim':(2, 12)},
        {'col': ['TecJet_Lambda1'], 'ylim':(1.5, 2.5)},
        {'col': ['Various_Values_TempMixture'], 'ylim':(40, 60)},
        {'col': ['Hyd_PressOilDif'], 'ylim':(0, 2)},
        {'col': ['Aux_PreChambDifPress'], 'ylim':(-1500, 1500)},
        ]

dat = {
    161: ['CountOph', 'h'],
    102: ['PowerAct', 'kW'],
    69: ['Hyd_PressCoolWat', 'bar']
}

dset2 = [{'col': ['PowerAct'], 'ylim':(0, 5000)},
         {'col': ['time']},
         {'col': ['diff']},
         ]
dmyplant2.chart(dfs, dset2, title=e, figsize=(12, 8))

# for i in range(len(dset) - 1):
#     ldset = dset[:(i+2)]
#     dmyplant2.chart(dfs, ldset, title=e, figsize=(12, 8))

plt.show()
