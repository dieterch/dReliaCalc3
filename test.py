

import dmyplant2
import arrow
import traceback

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


dmyplant2.cred()
mp = dmyplant2.MyPlant(3600)

try:
    # Version mit Engine_SN
    e = dmyplant2.Engine_SN(mp, 1320072)

    print(f"{e} {e.id}")

    dloc = e.Validation_period_LOC()

    #sys.exit(0)

    dmyplant2.chart(dloc, [
        {'col': ['LOC','OilConsumption'],'ylim': (0,1.6)},
        {'col': ['Pow'],'ylim': (0,8000)},
    ],
    title = e,
    figsize = (12,8))
    plt.show()


except Exception as e:
    print(e)
    traceback.print_tb(e.__traceback__)
