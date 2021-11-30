
import pylatextables.latex_table as tab

import numpy as np

# main


a = np.arange(0, 10)
b = a**2

table = tab.LatexTable([a,b], col_align='l', header=[r'$x$', r'$x^2$' ])
table.save_file('table.tex')

print(table)