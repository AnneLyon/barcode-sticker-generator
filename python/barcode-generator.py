import os
import time
from fpdf import FPDF
from barcode import Code128
from barcode.writer import ImageWriter

#initialiser katalog
outputdir = "temp/"
try:
    os.mkdir(outputdir)
except:
    pass
nameOfPdfFile = ""

#input data to initialize barcode generation
typeTekstInput = input("Skal du lage barkoder med medlemsnavn? Tast J for ja, eller N for nei: ")
if ((typeTekstInput == "J") or (typeTekstInput == "j")):
    navn = input("Lim inn en kommaseparert liste med navn: ")
    navneListe = navn.split(",")
     #generate barcodes and write as file to a temp directory
    for navn in navneListe:
        with open(outputdir + str(navn) + '.jpeg', 'wb') as f:
            Code128((str(navn)), writer=ImageWriter()).write(f)
        time.sleep(0.005)
        nameOfPdfFile = "generated-pdf/" + "medlemsnavn.pdf"
else:
    verkNavn = input("Navn på verk: ")
    index = input("Startnummer: ")
    to_index = input("Siste nummer: ")

    #generate barcodes and write as file to a temp directory
    while int(index) <= int(to_index):

        with open(outputdir + str(verkNavn) + str(index) + '.jpeg', 'wb') as f:
            Code128((str(verkNavn) + " " + str(index)), writer=ImageWriter()).write(f)
        index = int(index) + 1
        time.sleep(0.005)
        nameOfPdfFile = "generated-pdf/" + verkNavn + ".pdf"

#time.sleep(1)

#list the files with barcodes, and sort them by created date
generated = os.listdir(outputdir)
files = [os.path.join(outputdir, f) for f in generated] # add path to each file
files.sort(key=lambda x: os.path.getmtime(x))

#print the generated barcodes to the pdf file
margin = 5
y = margin
x = margin
col = 0
barCodeWidth = 60
barCodeHeight = 20
labelWidth = 70
labelHeight = 37
rownumber = 1
pdf = FPDF()
pdf.set_font('Times', '', 12)
pdf.add_page()
for image in files:
    print(image)
    pdf.image(image, x, y, barCodeWidth, barCodeHeight)
    x = x + labelWidth
    if x > margin + labelWidth * 2:
        rownumber = rownumber + 1
        x = margin
        y = y + labelHeight
    if rownumber > 8:
        rownumber = 1
        y = margin
        pdf.add_page()


# output the pdf file to the generated-pdf directory
pdf.output(nameOfPdfFile, "F")

#remove all temporary barcode files
for f in generated:
    os.remove(os.path.join(outputdir, f))
