from dmyplant2 import cred
import dmyplant2
import pandas as pd
from pprint import pprint as pp
import sys
import matplotlib.pyplot as plt
import arrow

dval = pd.read_csv("input2.csv", sep=';', encoding='utf-8')
# pp(dval['val start'])
dval['val start'] = pd.to_datetime(dval['val start'], dayfirst=True)
#print(dval.columns)

mp = dmyplant2.MyPlant(7200)
vl = dmyplant2.Validation(mp, dval, cui_log=False)


#failures = pd.DataFrame([])
#dmyplant2.demonstrated_Reliabillity_Plot(vl,beta=1.21, T=30000, s=1000, ft=failures, cl=[10, 50, 90], factor=2.0)

d = vl.dashboard
d.loc[:,('Name')]= d['Name'] + ' ' + d['Engine Type'] + ' ' + d['Engine Version'] + ' ' + d['Engine ID']
dc =  pd.concat([d[['Name','oph parts']], dval[['Old PU first replaced OPH','Old PUs replaced before upgrade']]],axis=1).set_index('Name').sort_values(by = "oph parts",ascending=True)
#print(dc)

dc.plot.barh(subplots=False, color=['blue','red','green'], figsize=(18,10), xlim=(0,8000), grid=True)
plt.subplots_adjust(left=0.3, right=0.95, top=0.95, bottom=0.05)
plt.show()

sys.exit(0)

# Please write SerialNumber of interesting Validation engine into sn: 
sn=1393153

for e in vl.engines:
    print(e)
    df = e.batch_hist_dataItems(itemIds={161: 'CountOph', 102: 'PowerAct'}, p_from=arrow.now('Europe/Vienna').shift(days=-7), p_to=arrow.now('Europe/Vienna'),timeCycle=3600)
    # Set Type of time column to DateTime
    df['datetime'] = pd.to_datetime(df['time'] * 1000000)
    df['CountOph'] = df.CountOph - e._d['oph@start']

    #dt = e.batch_hist_dataItems().plot(subplots=False, x='time', color=['red','black','blue'], secondary_y = ['CountOph'], figsize=(16,10))
    df.plot(subplots=True, x='datetime', color=['red','black','blue'], y = ['CountOph','PowerAct'], title = e, figsize=(16,10))

plt.show()

# print('----')
# for i, e in enumerate(vl.engines):
#    print(f"{i:02d} {e} {e.historical_dataItem(161, e.now_ts):6.0f} oph")
