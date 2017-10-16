import hashlib
import os
from urllib import request
import urllib

def MD5(fname):
    hash_md5 = hashlib.md5()
    with open(fname,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest().encode('utf-8','strict').decode('utf-8')

filename = input()
md5 = MD5(filename)
mdurl = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + filename + ".md5"
mdWebFile = urllib.request.urlopen(mdurl)
mdline = mdWebFile.read().decode("utf-8").strip().split(" ")
print(md5)
print(mdline[1])
print(md5 == mdline[1])