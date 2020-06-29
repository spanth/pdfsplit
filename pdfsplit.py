import sys
import os
import re
import getopt
from PyPDF2 import PdfFileWriter, PdfFileReader

def split_pdf(input_file, output_file, pages):
    fp = open(input_file, "rb")
    inputpdf = PdfFileReader(fp)
    
    if inputpdf.isEncrypted:
        try:
            inputpdf.decrypt('')
            print('File Decrypted (PyPDF2)')
        except:
            command = ("cp "+ input_file +
                   " temp.pdf; qpdf --password='' --decrypt temp.pdf " + input_file
                   + "; rm temp.pdf")
            os.system(command)
            print('File Decrypted (qpdf)')
            fp = open(input_file)
            inputpdf = PdfFileReader(fp)
    
    outputpdf = PdfFileWriter()

    newpages = []
    for p in pages:
        if '-' in p:
            num_range = p.split('-')
            for r in range(int(num_range[0]),int(num_range[1])+1):
                newpages.append(r)
        else:
            newpages.append(p)

    print (newpages)
    pages_int = [int(x) for x in newpages]
    
    for i in pages_int:
        outputpdf.addPage(inputpdf.getPage(i - 1))
    with open(output_file, "wb") as outf:
        outputpdf.write(outf)


def main(argv):
    try:
        INPUT = argv[0]
        OUTPUT = argv[1]
        PAGES = argv[2:]
    except:
        usage()
        sys.exit(2)
    
    split_pdf(INPUT, OUTPUT, PAGES)


def usage():
    print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
