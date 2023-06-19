from PyPDF2 import PdfFileReader, PdfFileWriter

reader = PdfFileReader("ProblemTransformationNew1.pdf", "r")

page = reader.getPage(0)

print(page.cropBox.getLowerLeft())
print(page.cropBox.getUpperLeft())
print(page.cropBox.getLowerRight())
print(page.cropBox.getUpperRight())

writer = PdfFileWriter()
#page.cropBox.setLowerLeft((page.cropBox.getLowerLeft()[0], page.cropBox.getLowerLeft()[1] - 2 * page.cropBox.getLowerLeft()[1]/3))
#page.cropBox.setLowerRight((page.cropBox.getLowerRight()[0], page.cropBox.getLowerRight()[1] - 2 * page.cropBox.getLowerRight()[1]/3))

a = 0
b = 400
c = 0
d = b
page.cropBox.setLowerLeft((page.cropBox.getUpperLeft()[0], int(page.cropBox.getUpperLeft()[1] - b)))
page.cropBox.setLowerRight((page.cropBox.getUpperRight()[0], int(page.cropBox.getUpperRight()[1] - d)))



writer.addPage(page)


with open("ProblemTransformationNew.pdf", "wb") as file:
    writer.write(file)
print(page.cropBox.getLowerLeft())
print(page.cropBox.getUpperLeft())
print(page.cropBox.getLowerRight())
print(page.cropBox.getUpperRight())