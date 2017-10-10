import urllib.request
import os
import time
import gzip


number = "0001"
file = "medline"

#filenumber = input the file number on pubMed Database
#this will download the file ./src/zip and extract to ./src/raw
#func will return the unzipped file path
def dlext(filenumber):
    number = "{:04}".format(filenumber)
    file = "medline17n" + number + ".xml.gz"
    url = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + file
    if not os.path.exists('./src/zip'):
            os.makedirs('./src/zip')
    path = os.path.join("./src/zip",file)
    
    if os.path.exists(path):
        print('Already got ' + file + ' proceeding to next step...')
    else:
        print("Downloading "+file)
        trycount = 0
        while(trycount<5):
            try:
                urllib.request.urlretrieve(url,path,reporthook)
            except urllib.error.ContentTooShortError:
                print('Download failed for some reason, retrying')
                trycount+=1
                continue
        if trycount < 5:
            print(file + " Downloaded")
        else:
            print('download retry limit reached')
            os.remove(path)

    print('unzipping ' + file)
    with gzip.open(path, "rb") as zf:
        unzipfile = "medline" + number + ".xml"
        if not os.path.exists('./src/raw'):
            os.makedirs('./src/raw')
        unzippath = os.path.join('./src/raw', unzipfile)
        with open(unzippath,"wb") as of:
            of.write(zf.read())
        print('unzipped ' + file)

    time.sleep(20)
    return unzippath

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = ((readsofar * 1e2 / totalsize) // 0.01) /100
        print(str(percent) + '%',end='\r')
        if readsofar >= totalsize: # near the end
            print()
    else: # total size is unknown
        print('total size is unknown. Downloading...')