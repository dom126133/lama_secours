from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import pandas as pd
import numpy as np
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def pdf(shift_definition):
    logging.debug(shift_definition)

    #data = {'Account Name': ['ACCOUNT PAYABLE', 'PAGIBIG LOAN PAYABLE','PREPAID TAX']
    #            ,'': [-0.1, -0.2,-0.3]}
    #summary_debit = pd.DataFrame(data=data)
    
    #colwidths = 50
    #GRID_STYLE = TableStyle(
    #            [('GRID', (0, 0), (-1, -1), 0.25, colors.pink),
    #            ('ALIGN', (1, 0), (-1, -1), 'RIGHT')])
    
    #t1 = Table([summary_debit.iloc[:,1].tolist(),summary_debit.iloc[:,0].tolist()]);
    #t1 = Table(np.array(summary_debit).tolist());
    t1 = Table(np.array(shift_definition).tolist(), colWidths=[50,100,100,200]);
    print(shift_definition.columns.values)
    print(t1)
    doc = SimpleDocTemplate("table.pdf", pagesize=A4)
    element = []
    element.append(t1)
    doc.build(element)
    return t1