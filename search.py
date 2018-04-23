import xml.etree.ElementTree as ET
import os

def check_pmid(fileroot,pmid_list):
    if int(fileroot.find('MedlineCitation').find('PMID').text) in pmid_list:
        return True
    else:
        return False

def check_abstract(fileroot):
    if fileroot.find('MedlineCitation').find('Article').find('Abstract') != None \
        or fileroot.find('MedlineCitation').find('OtherAbstract') != None:
        return True
    else:
        return False
