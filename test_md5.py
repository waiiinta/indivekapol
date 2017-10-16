import hashlib
import os
import urllib

def MD5(fname):
    hash_md5 = hashlib.md5()
    with open(fname,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

filename = input()
md5 = MD5(filename)
mdurl = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' + filename + ".md5"
mdWebFile = urllib.request.urlopen(mdurl)
mdline = mdWebFile.readlines()
print(mdline)