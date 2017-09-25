import urllib.request
import os
import time

number = "0001"
file = "medline"

for i in range(1,9):
    number = "{:04}".format(i)
    file = "medline17n" + number + ".xml.gz"
    url = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + file
    path = os.path.join("D:/INDIV/src/",file)
    urllib.request.urlretrieve(url,path)
    print("Downloading "+file)
    time.sleep(20)
