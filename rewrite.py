import xml.etree.ElementTree as ET
import os

#file = file directory of the file you want to rewrite example ./input/blahblah.xml
#outfile = file directory where you want to store the rewrited file example ./output/blahblah.xml
def rewrite(file,outfile):
    print("parsing " + file + "in tree...")
    tree = ET.parse(file)
    root = tree.getroot()
    medlineCitationGetlist = ['PMID','MedlineJournalInfo','DateCreated','Article','KeywordList','OtherAbstract','MeshHeadingList']
    medlineCitationRmlist = ['DateCompleted','DateRevised','MedlineJournalInfo','ChemicalList','CitationSubset']


    #looping PubmedArticleSet
    print("Rewriting...")
    medlineCitation = root[0]

    #remove pubMedData
    root.remove(root[1])

    #loop each child in medLineCitation and remove what we don't want
    for child in medlineCitation:
        if not child.tag in medlineCitationGetlist:
            medlineCitation.remove(child)



    # for child in medlineCitation:
    #     if child.tag in Medlinecitationrmlist:
    #         medlineCitation.remove(child)
    tree.write(outfile)