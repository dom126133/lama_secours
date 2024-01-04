from reportlab.pdfgen import canvas
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
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

    doc = SimpleDocTemplate("table.pdf", pagesize=A4)
    styles = getSampleStyleSheet()

    title = Paragraph('Tour XXX', style=styles['h1'])
    generated_timestamp = Paragraph(f"Generated using data from XXX.", style=styles['Normal'])
    t1 = Table(shift_definition, colWidths=[30*mm,30*mm,140*mm]);


    element = []
    element.append(title)
    element.append(generated_timestamp)
    element.append(t1)
    doc.build(element)
    return t1