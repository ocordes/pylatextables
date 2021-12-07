"""

written by: Oliver Cordes 2021-11-30
changed by: Oliver Cordes 2021-12-07
"""

import numpy as np



class LatexTable(object):
    def __init__(self, data,
                header=None,
                header_bottom_hline=True,
                header_top_hline=False,
                footer_hline=False,
                col_type='c',
                col_descr=None     # overwrite the col_description, default is col_type for all colums
                ):
        """
        Initialise a LatexTable object with all data structures. The LaTeX table will be created with __str__
        or save_file method. This methods checks all parameters carefully and raises TypeError- and ValueError-error
        upon wrong used parameters.

        Parameters
        ----------
        data: list or tuple
            List of data columns.
        header: list or tuple, optional
            List of header strings to describe the tabular data. The number of entries must be
            the same as the number of data columns.
        header_bottom_hline: bool, optional
            Prints a line below the header.
        header_top_hline: bool, optional
            Prints a line above the header.
        footer_hline: bool, optional
            Prints a line at the end of the table.
        col_type: char, optional
            Type of all columns in LaTeX coding, 'l', 'c', 'r', 'S' (from siunitx).
        col_descr: list or tuple, optional
            Sets the col_type individually for all columns. The number of entries must be the same
            as the number of data columns. (There is no check of correctness!)
        """

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
            self._col_type = col_type
        else:
            self._col_descr = col_descr
            self._col_type = None


        # check for header descriptions
        if header is not None:
            if isinstance(header, (list, tuple)):
                if len(header) != self._nritems:
                    raise ValueError('header must have same length as number of columns')
                if (self._col_type is not None) and (self._col_type == 'S'):   
                    # change for siunitx
                    header = ['{%s}' % i for i in header]

            else:
                raise ValueError('header must be list or tuple')
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
        """
        Converts the data columns into a LaTeX table represented as an ascii string.
        """
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
        """
        Saves the table into filename.

        Parameters:
        -----------
        filename: The name of the file to save the table.
        """
        with open(filename, mode='w' ) as f:
            f.write(self.__str__())
