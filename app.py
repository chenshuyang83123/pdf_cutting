from PyPDF2 import PdfFileReader, PdfFileWriter
import os, sys, shutil

def cutting(filename, side_cut_precent=0.25):
    current_stream = open(filename, 'rb')
    pdf_input = PdfFileReader(current_stream, strict = False)
    page_count = pdf_input.getNumPages()
    pdf_output = PdfFileWriter()

    for i in range(page_count):
        page = pdf_input.getPage(i)
        
        old_width = float(page.mediaBox.getUpperRight_x())
        old_high = float(page.mediaBox.getUpperRight_y())

        page.mediaBox.lowerLeft = (old_width*side_cut_precent , 0)
        page.mediaBox.lowerRight = (old_width*(1-side_cut_precent), 0)
        page.mediaBox.upperLeft = (old_width*side_cut_precent, old_high)
        page.mediaBox.upperRight = (old_width*(1-side_cut_precent), old_high)
        pdf_output.addPage(page)
    
    with open('./tmp.pdf', "wb") as new_stream:
        pdf_output.write(new_stream)
        
    current_stream.close()
    new_stream.close()

    os.remove(filename)
    shutil.copyfile('./tmp.pdf', filename)

if __name__ == '__main__':
    print('start')
    print(sys.argv)
    if len(sys.argv) == 1:
        print('I need a folder')
        sys.exit()
    folder = sys.argv[1]
    files= os.listdir(folder)
    s = []

    for file in files:
        if str(file).lower().__contains__('.pdf'):
            fullname = folder + '/' + str(file)
            print(fullname)
            cutting(fullname)
