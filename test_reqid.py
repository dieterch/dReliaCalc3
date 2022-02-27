from dmyplant2 import HandleID
import pandas as pd
from tabulate import tabulate
from pprint import pprint as pp
import sys


dat0 = {
    161: ['Count_OpHour', 'h'],
    102: ['Power_PowerAct', 'kW'],
    217: ['Hyd_PressCrankCase', 'mbar'],
    16546: ['Hyd_PressOilDif', 'bar'],
    69: ['Hyd_PressCoolWat', 'bar'],
}

try:
    r = HandleID(filename='DataItems_Request.csv')
    print(r.unit(name='Power_PowerAct'))
    print(r.unit(id=102))

    r = HandleID(datdict=dat0)
    print(r.unit(name='Hyd_PressCrankCase'))
    print(r.unit(id=217))
    pp(r.datdict())
except Exception as e:
    print(e)