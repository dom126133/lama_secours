from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import pandas as pd
import numpy as np
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def pdf(shift_definition):
    logging.debug(shift_definition)
    for task in shift_definition:
        task[2] = Paragraph(task[2])
        #print(task[2])

    t1 = Table(shift_definition, colWidths=[30*mm,30*mm,140*mm]);

    doc = SimpleDocTemplate("table.pdf", pagesize=A4)
    element = []
    element.append(t1)
    doc.build(element)
    return t1