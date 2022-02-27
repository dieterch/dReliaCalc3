from datetime import datetime
import logging
import os
import pandas as pd
import xlwings as xw

#from pprint import pprint as pp

class ExcelHandler:
    """
    Handle Excel In/Out put
    wrapping xlwings
    CAUTION: specific EXCEL File Format required.

    see ndreliacalc4.xlsx
    """
    _wb = None
    _val = None
    _dat = None

    def __init__(self, VAL):
        """
        Open Excel Workbook VAL and check BC's
        e.g.: xl = ExcelHandler(VAL)
        """
        f = os.getcwd() + '/' + VAL

        try:
            self._wb = xw.Book(f)
        except FileNotFoundError:
            logging.error(f"{f} not found.")
            raise

    def openfile(self):
        """
        opens the VAL File
        writes "'Update in progress' into Excelsheet ndashboard Cell B2"
        returns content of "validation" sheet as pandas DataFrame 
        """
        # xl.names()
        self._write('ndashboard', 'B2', 'Update in progress')
        return (self.val, self.cacheing)

    @property
    def val(self):
        """
        returns content of "validation" sheet as pandas DataFrame         
        """
        self._val = self._wb.sheets['validation'].range('A1') \
            .options(pd.DataFrame, header=1, index=False, numbers=int, expand='table').value
        return self._val

    @property
    def cacheing(self):
        """
        reads Cell F2 in 'validation' and
        returns this value as cacheing time
        """
        return int(self._read('ndashboard', 'F2'))

    def _read(self,  Sheet, Cell):
        """
        internal
        _read(sheet, cell) function
        """
        return self._wb.sheets(Sheet).range(Cell).value

    def _write(self, Sheet, Cell, Value):
        """
        internal
        _write(sheet, cell, value) function
        """
        self._wb.sheets(Sheet).range(Cell).value = Value

    def names(self):
        """
        print defined Names in EXCEL
        implemented for debug reasons
        """
        names = [name.name for name in self._wb.names]
        for name in names:
            print(f"{name} {self._wb.names[name].refers_to}")

    # def UpdateNames(self, rows):
    #     """
    #     change Excel Names content
    #     implemented for debug resons
    #     originally meant to change Data Areas
    #     according to the Validation Input
    #     works with extended, provisioned areas too. 
    #     """
    #     data_rv = str(rows + 4)
    #     prop_rv = str(rows + 4)
    #     val_rv = str(rows + 1)
    #     self._wb.names.add('data_i', "=dataItems!$A$5:$A$" + data_rv)
    #     self._wb.names.add('data_val', "=dataItems!$A$5:$JNC$" + data_rv)
    #     self._wb.names.add('prop_i', "=properties!$A$5:$A$" + prop_rv)
    #     self._wb.names.add('prop_val', "=properties!$A$5:$CB$" + prop_rv)
    #     self._wb.names.add('val_i', "=validation!$A$2:$A$" + val_rv)
    #     self._wb.names.add('val_val', "=validation!$A$2:$F$" + val_rv)

    def UpdateVAL(self, vl):
        """
        Write the data into the EXCEL
        inform about progress on command line ....
        Write "Date & Time into Excelsheet ndashboard Cell B2"
        """
        # xl.write('dashboard', 'A4', dash)
        logging.info(f"Copy properties to Excel ...")
        self._write('properties', 'A4', vl.properties)
        logging.info(f"Copy dataItems to Excel ...")
        self._write('dataItems', 'A4', vl.dataItems)
        logging.info(f"Copy properties keys in dictionary ...")
        self._write('dictionary', 'H3', vl.properties_keys)
        logging.info(f"Copy dataItems keys in dictionary ...")
        self._write('dictionary', 'P3', vl.dataItems_keys)

        # xl.UpdateNames(100)
        # Update current date
        today = datetime.now()
        self._write('ndashboard', 'B2', today)
