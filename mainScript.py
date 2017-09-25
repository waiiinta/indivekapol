import xml.etree.ElementTree as ET

print("parsing xml in tree...")
tree = ET.parse('./medline17n0001.xml/medline17n0001.xml')
root = tree.getroot()
medlineCitationGetlist = ['PMID','MedlineJournalInfo','DateCreated','Article','KeywordList','OtherAbstract','MeshHeadingList']


#looping PubmedArticleSet
print("Creating new xml...")
for pubMedArticle in root:
    medlineCitation = pubMedArticle[0]

    #remove pubMedData
    pubMedArticle.remove(pubMedArticle[1])

    #loop each child in medLineCitation and remove what we don't want
    for child in medlineCitation:
        if not child.tag in medlineCitationGetlist:
            medlineCitation.remove(child)



# for child in medlineCitation:
#     if child.tag in Medlinecitationrmlist:
#         medlineCitation.remove(child)
tree.write('new2.xml')