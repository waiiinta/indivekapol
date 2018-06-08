import xml.etree.ElementTree as ET
import os

#file = file directory of the file you want to rewrite example ./input/blahblah.xml
def rewrite(file):
    tree = ET.parse(file)
    root = tree.getroot()
    medlineCitationGetlist = ['PMID','MedlineJournalInfo','DateCreated','Article','KeywordList','OtherAbstract','MeshHeadingList']
    medlineCitationRmlist = ['DateCompleted','DateRevised','MedlineJournalInfo','ChemicalList','CitationSubset']


    #looping PubmedArticleSet
    medlineCitation = root[0]

    #remove pubMedData
    root.remove(root[1])

    #loop each child in medLineCitation and remove what we don't want
    for child in medlineCitation:
        if not child.tag in medlineCitationGetlist:
            medlineCitation.remove(child)

    tree.write(file,encoding="utf-8")

def fix_encode(file):
    tree = ET.parse(file,parser=ET.XMLParser(encoding="utf-8"))
    tree.write(file,encoding="utf-8")

def update_pmid(file,update_file):
    read_file = open(file,'r')
    old_file = open(update_file,'r')
    new_pmid = sorted([int(i) for i in read_file.readlines()])
    old_pmid = sorted([int(i) for i in old_file.readlines()])
    
    update_pmid = set()

    for pmid in old_pmid:
        update_pmid.add(pmid)
    
    for pmid in new_pmid:
        update_pmid.add(pmid)

    read_file.close()
    old_file.close()

    print(len(old_pmid))
    print(len(new_pmid))
    print(len(update_pmid))
    write_file = open(update_file,'w')

    for pmid in update_pmid:
        write_file.write(str(pmid)+"\n")
