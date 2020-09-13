#!/usr/bin/env python3
import re, os, glob, sys, subprocess
from collections import defaultdict as dd

try:
    import PyPDF3
except ImportError:
    ask = input("\nPyPDF3 package not found\nPress [y/Y] and ENTER to install and proceed with your search...")
    if ask == "y" or ask == "Y":
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF3"])
        os.system('cls' if os.name == 'nt' else 'clear')
        import PyPDF3
    else:
        sys.exit(1)

targetFolder = os.getcwd()+"/target/"
pdfFiles = [file for file in glob.glob(targetFolder + "*.pdf")]

def search(query):
    results = []
    if query is not None:
        for pdf in pdfFiles:
            pdfName = "PDF_NAME: "+pdf.split('/')[-1]
            try:
                fileObject = PyPDF3.PdfFileReader(pdf)
                numPages = fileObject.getNumPages()
                for page in range(0, numPages):
                    pageObj = fileObject.getPage(page)
                    searchResults = re.search(query, pageObj.extractText(), re.IGNORECASE)
                    if searchResults:
                        pageResult = ("Page: {}".format(str(page+1)))
                        results.append((pdfName, pageResult))
            except PyPDF3.utils.PdfReadError:
                pass
        write(query, results)

def write(query, inputDict):
        if inputDict:
            results = dd(list)
            for key, val in inputDict:
                results[key].append(val)
            for data in sorted(results.keys()):
                print("\n"+data+":", end="\n\t")
                print(*results[data], sep="\n\t")
        else:
            print("No results found")
        sys.exit(0)

if __name__ == "__main__":
    if pdfFiles:
        try:
            search(sys.argv[1])
        except IndexError:
            print("\tNo 'input detected, Please refer README.md'")
            sys.exit(1)
    else:
        print("\tNo 'target' directory found, Please refer README.md")
        sys.exit(1)
