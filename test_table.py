
#import pylatextables.latex_table as tab
import pylatextables as tab

import numpy as np

# main


a = np.arange(0, 10, dtype=np.float64)
b = a / 7

table = tab.LatexTable([a,b], 
                        use_booktabs=True,
                        col_type='S', 
                        col_siunitx=None,
                        header=[r'$x$', r'$x^2$' ])
table.save_file('table.tex')

print(table)