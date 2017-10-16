from urllib import request
import urllib
import os
import time
import gzip
import hashlib


number = "0001"
file = "medline"

#filenumber = input the file number on pubMed Database
#this will download the file ./src/zip and extract to ./src/raw
#if download is successful, it will extract the file and return the unzipped path
#if download is failed, it will return "DOWNLOAD FAILED"

def MD5(fname):
    hash_md5 = hashlib.md5()
    path = os.path.join("./src/zip",fname)
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

def dlext(filenumber):
    downloaded = False
    number = "{:04}".format(filenumber)
    file = "medline17n" + number + ".xml.gz"
    url = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + file
    if not os.path.exists('./src/zip'):
            os.makedirs('./src/zip')
    path = os.path.join("./src/zip",file)
    
    print("Downloading "+file)
    trycount = 0
    while(trycount<5):
        try:
            urllib.request.urlretrieve(url,path,reporthook)
            break
        except urllib.error.ContentTooShortError:
            print('Download failed for some reason, retrying')
            trycount+=1
            continue
    if trycount < 5:
        print(file + " Downloaded")
        downloaded = True
    else:
        print('download retry limit reached')
        os.remove(path)

    if downloaded:
        print("checking"+file+"isn't corrupt")
        md5 = MD5(path)
        mdurl = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + file + ".md5"
        mdWebFile = urllib.request.urlopen(mdurl)
        mdline = mdWebFile.read().decode("utf-8").split(" ")
        if md5 == mdline:
            check = True
            print()
        else:
            check = False  
        
        print('unzipping ' + file)
        with gzip.open(path, "rb") as zf:
            unzipfile = "medline17n" + number + ".xml"
            if not os.path.exists('./src/raw'):
                os.makedirs('./src/raw')
            unzippath = os.path.join('./src/raw', unzipfile)
            with open(unzippath,"wb") as of:
                of.write(zf.read())
            print('unzipped ' + file)

        time.sleep(20)
        return unzippath
    else:
        #????? what should we return????
        return 'DOWNLOAD FAILED'

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = ((readsofar * 1e2 / totalsize) // 0.01) /100
        print(str(percent) + '%',end='\r')
        if readsofar >= totalsize: # near the end
            print()
    else: # total size is unknown
        print('total size is unknown. Downloading...')