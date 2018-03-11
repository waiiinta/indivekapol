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

def MD5(path):
    hash_md5 = hashlib.md5()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

def dlext(filenumber,logfile):
    downloaded = False
    number = "{:04}".format(filenumber)
    file = "medline17n" + number + ".xml.gz"
    url = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + file
    if not os.path.exists('./src/zip'):
            os.makedirs('./src/zip')
    path = os.path.join("./src/zip",file)
    
    print("Downloading "+file)
    logfile.write("Downloading" + file + "\r\n")
    trycount = 0
    while(trycount<5):
        time.sleep(90)
        try:
            urllib.request.urlretrieve(url,path,reporthook)
            break
        except:
            print('Download failed for some reason, retrying')
            logfile.write('Download failed for some reason, retrying\r\n')
            trycount+=1
            time.sleep(30)
            continue
    if trycount < 5:
        print(file + " Downloaded")
        logfile.write(file + " Downloaded\r\n")
        downloaded = True
    else:
        print('download retry limit reached')
        logfile.write('download retry limit reached\r\n')
        os.remove(path)

    if downloaded:
        print("checking"+file+"isn't corrupt")
        logfile.write("checking"+file+"isn't corrupt\r\n")
        md5 = MD5(path)
        mdurl = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + file + ".md5"
        mdWebFile = urllib.request.urlopen(mdurl)
        mdline = mdWebFile.read().decode("utf-8").strip().split(" ")
        if md5 == mdline[1]:
            check = True
            print(file + " isn't corrupt.")
            logfile.write(file + " isn't corrupt\r\n")
        else:
            check = False
            # if os.path.exists('logfile.txt'):
            #     append_write = 'a'
            # else:
            #     append_write = 'w'
            # Don't know what we must return.
            # log = open("logfile.txt",append_write)
            # log.write(file + " IS CORRUPT\n")
            # log.close()
            print(file + " is corrupt !!!")
            logfile.write(file + " is corrupt !!!\r\n")
        
        if check:
            print('unzipping ' + file)
            logfile.write('unzipping ' + file+"\r\n")
            with gzip.open(path, "rb") as zf:
                unzipfile = "medline17n" + number + ".xml"
                if not os.path.exists('./src/raw'):
                    os.makedirs('./src/raw')
                unzippath = os.path.join('./src/raw', unzipfile)
                with open(unzippath,"wb") as of:
                    of.write(zf.read())
                print('unzipped ' + file)
                logfile.write('unzipped ' + file+ "\r\n")

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