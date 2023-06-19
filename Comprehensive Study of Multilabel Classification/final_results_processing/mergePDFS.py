from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import os


path = "/home/jasminb/PycharmProjects/Process_dataSets/Paper_Reults/Algorithm_adaptation_methods/pdfs/"
pdfs = os.listdir(path)


def changePDFs():
    for pdf in pdfs:

        metric = pdf
        pathToStore = path + pdf

        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)

        can.drawString(10, 100, metric)
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open(pathToStore, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open(pathToStore, "wb")
        output.write(outputStream)
        outputStream.close()

def pdfMerge():
    merger = PdfFileMerger()


    for pdf in pdfs:
        merger.append(path + pdf)

    merger.write("AlgorithmAdaptation.pdf")
    merger.close()

#changePDFs()
pdfMerge()


