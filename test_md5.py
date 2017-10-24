import hashlib
import os
from urllib import request
import urllib

def MD5(fname):
    hash_md5 = hashlib.md5()
    with open(fname,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

def testDownload(fname):
    url = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + fname
    if not os.path.exists('./src/zip'):
            os.makedirs('./src/zip')
    path = os.path.join("./src/zip",fname)
    
    print("Downloading "+fname)
    urllib.request.urlretrieve(url,path,reporthook)

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = ((readsofar * 1e2 / totalsize) // 0.01) /100
        print(str(percent) + '%',end='\r')
        if readsofar >= totalsize: # near the end
            print()
    else: # total size is unknown
        print('total size is unknown. Downloading...')

filename = input()
for i in range(2):
    testDownload(filename)
    if i == 0:
        print("hi")
md5 = MD5(filename)
mdurl = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + filename + ".md5"
mdWebFile = urllib.request.urlopen(mdurl)
mdline = mdWebFile.read().decode("utf-8").strip().split(" ")
print(md5)
print(mdline[1])
print(md5 == mdline[1])