"""

written by: Oliver Cordes 2021-11-30
changed by: Oliver Cordes 2021-11-30
"""

import numpy as np


class LatexTable(object):
    def __init__(self, data,
                header=None,
                header_bottom_hline=True,
                header_top_hline=False,
                footer_hline=False,
                col_type='c',
                col_descr=None     # overwrite the col_description, default is col_align for all colums
                ):

        self._length = -1
        self._check_data(data)   # if error it will never come back ...

        # save some information
        self._data = data
        self._nritems = len(data)

        # handle the columnn descriptions
        if col_descr is None:
            if col_type not in ['c', 'l', 'r', 'S']:
                raise ValueError('col_type must be one of \'l\',\'c\',\'r\',\'S\'')
            self._col_descr = ''.join([col_type for i in range(self._nritems)])
        else:
            self._col_descr = col_descr


        # check for header descriptions
        if header is not None:
            if isinstance(header, (list, tuple)):
                if len(header) != self._nritems:
                    raise ValueError('header must have same length as number of columns')
        self._header = header
        self._header_top_hline = header_top_hline
        self._header_bottom_hline = header_bottom_hline
        self._footer_hline = footer_hline
        

    def _check_data(self, data):
        # check if data is list or tuple
        if isinstance(data, (list, tuple)):
            self._data = data
        else:
            raise TypeError('TableData must be list or tuple')

        if len(data) == 0:
            raise TypeError('TableData is empty')

        # check if columns are lists/tuples or numpy arrays and have same length
        for i in data:
            if isinstance(i, (list, tuple, np.ndarray)):
                if isinstance(i, np.ndarray):
                    if i.ndim > 1:
                        raise TypeError('numpy array must have only one dimension')
                if self._length == -1:
                    self._length = len(i)
                else:
                    if len(i) != self._length:
                        raise TypeError('Columns have different length')
            else:
                raise TypeError('Column must be list, tuple or np.ndarray')


    def __str__(self):
        s = '\\begin{tabular}{'+self._col_descr+'}\n'
        if self._header_top_hline:
            s += '\\hline \n'
        if self._header is not None:
            for cols in range(self._nritems):
                s += f'{self._header[cols]}'
                if cols < (self._nritems-1):
                    s += ' & '
            s += ' \\\\ \n'

        if self._header_bottom_hline:
            s += '\\hline \n'

        for lines in range(self._length):
            for cols in range(self._nritems):
                s += f'{self._data[cols][lines]}'
                if cols < (self._nritems-1):
                    s += ' & '
            s += ' \\\\ \n'

        if self._footer_hline:
            s += '\\hline \n'

        s += '\\end{tabular} \n'
        return s


    def save_file(self, filename):
        with open(filename, mode='w' ) as f:
            f.write(self.__str__())