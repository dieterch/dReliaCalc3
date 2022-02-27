import dmyplant2
from dmyplant2 import cred, Validation, MyPlant
from dExcelHandler import ExcelHandler
import logging
import sys
import traceback

global DEBUG
DEBUG = True

logging.basicConfig(
    filename='dmyplant.log',
    filemode='w',
    format='%(asctime)s %(levelname)s, %(message)s',
    level=logging.INFO
)
hdlr = logging.StreamHandler(sys.stdout)
logging.getLogger().addHandler(hdlr)

# Validation Excel Workbook Name
# needs to be in the current working directory
VAL = 'ndReliaCalc4.xlsx'


def main():
    try:
        logging.info('---')
        logging.info('dReliaCalc Application Started')

        xl = ExcelHandler(VAL)
        dval, cacheing = xl.openfile()

        logging.info(f"MyPlant Data Cache {cacheing} s")

        cred()
        mp = MyPlant(cacheing)  # no parameter = 7200s caching time
        vl = Validation(mp, dval)

        dash = vl.dashboard
        dash = dash.sort_values('oph parts', ascending=False)
        dash.reset_index(drop=True, inplace=True)
        # pp(dash)  # print dashboard to Terminal

        xl.UpdateVAL(vl)

        logging.info('dReliaCalc successfully completed.')
        logging.info('---')

    except Exception as e:
        print(e)
        if DEBUG:
            traceback.print_tb(e.__traceback__)
    finally:
        hdlr.close()
        logging.getLogger().removeHandler(hdlr)


if __name__ == '__main__':
    main()
