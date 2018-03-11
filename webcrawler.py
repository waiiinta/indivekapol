from urllib.request import urlopen,Request 
from bs4 import BeautifulSoup 
import requests
import re
import time
from pathlib import Path
import sys

omic_category = ["https://omictools.com/genomics2-category",
                "https://omictools.com/epigenomics-category",
                "https://omictools.com/transcriptomics-category",
                "https://omictools.com/proteomics-category",
                "https://omictools.com/metabolomics-category",
                "https://omictools.com/phenomics-category",
                "https://omictools.com/text-mining-category"]

print("Crawler Start.")
print("First Stage,Crawling subcategory start.")
if Path('omictool_subcategory.txt').is_file():
        print(' Detect the file contains list of subcategory')
else:
        try:
                subcategory={}
                subcategory_file = open("omictool_subcategory.txt","w+")
                for category in omic_category:
                        subc_link = []
                        print("\r"+" Sending Request",end="")
                        response = requests.get(category)
                        categorylink = BeautifulSoup(response.text,"html5lib")
                        links = categorylink.findAll("a")
                        #print("\n"+category+"\n")
                        print("\r"+" Scraping "+category,end=" ")
                        for link in links:
                                href = link.get('href')
                                if href != None and \
                                        len(href) > 8 and \
                                        link.get('href')[len(href)-8:len(href)] == "category" and \
                                        link.get('href')[0] == "/": 
                                        subc_link.append(link.get('href'))
                                        subcategory_file.write(link.get('href')+"\n")
                        subcategory[category] = subc_link
                        print("DONE.")
                        time.sleep(5)
                        #print(subcategory[category])
                subcategory_file.close()
        except KeyboardInterrupt:
                print('\n'+"Program get interrupted")
                subcategory_file.close()
                print('Delete unfinished file')
                Path('omictool_subcategory.txt').unlink()
                print("Exit Program")
                sys.exit(1)
        except Error as e:
                print("e")
                print('Delete unfinished file')
                Path('omictool_subcategory.txt').unlink()
                print("Exit Program")
                sys.exit(1)

print("Crawling First Stage Finish.")
print("Second stage,crawling list-page of tools start.")
if Path('omictool_list_page.txt').is_file():
        print(' Detect the file contains the list of list-page of tools start')
else:
        try:
                listpage = {}
                listpage_list = []
                subcategory_file = open("omictool_subcategory.txt","r")
                listpage_file = open("omictool_list_page.txt","w+")
                for link in subcategory_file:
                        listpage_link = []
                        omiclink = "https://omictools.com"+link.strip()
                        print("\r Send Request",end="")
                        response = requests.get(omiclink)
                        sublink = BeautifulSoup(response.text,"html5lib")
                        group = sublink.findAll("div",{"class":"category-cards-container"})
                        print("\r Scraping "+omiclink,end=" ")
                        for member in group:
                                a_list = member.findAll('a')
                                for a in a_list:
                                        listpage_href = a.get('href')
                                        if listpage_href != None and \
                                                len(listpage_href) > 8 and \
                                                link.get('href')[len(listpage_href)-8:len(listpage_href)] == "category" and \
                                                link.get('href')[0] == "/": 
                                                listpage_link.append(link.get('href'))
                                                listpage_list.append(link.get('href'))
                        listpage[link] = listpage_link
                        print("DONE.")
                        time.sleep(3)
                listpage_file.close()
        except KeyboardInterrupt:
                print('\n'+"Program get interrupted")
                subcategory_file.close()
                print('Delete unfinished file')
                Path('omictool_subcategory.txt').unlink()
                print("Exit Program")
                sys.exit(1)
        except Error as e:
                print("e")
                print('Delete unfinished file')
                Path('omictool_subcategory.txt').unlink()
                print("Exit Program")
                sys.exit(1)

print("Second Stage Finish.")
print("Third Stage,crawling paper from list page.")
tool_list = []
for listpage in listpage_list:
        omiclist_link = "https://omictools.com"+listpage
        print("\r Send Request",end="")
        response = requests.get(omiclist_link)
        paperlist_page = BeautifulSoup(response.text,"html5lib")
        totalpage = paperlist_page.findAll("a",{"class":"tool-info-link"})
        
        tool_group = paperlist_page.findAll("a",{"class":"tool-info-link"})
        print("\r Scraping "+omiclink,end=" ")
        for tool in tool_group:
                tool_href = tool.get('href')
                if tool_href != None and \
                        len(href) > 8 and \
                        tool.get('href')[len(href)-8:len(href)] == "category" and \
                        tool.get('href')[0] == "/": 
                        tool_list.append(link.get('href'))

print("Third Stage Finish.")
print("Tool list :")
print(tool_list)
        





# omic_pmid = {}

# for link in links:
#     # print(link.get('href'))
#     if link.get('href')[0:28] == "/url?q=https://omictools.com":
#         print("Finding PMID")
#         omic_response = requests.get("https://www.google.co.th" + link.get('href'))
#         omic_html = BeautifulSoup(omic_response.text,"html5lib")
#         pmid = omic_html.findAll("span",attrs={"style":"margin-right: 20px"})
#         omic_pmid[link.get('href')] = pmid
#         #  = BeautifulSoup(response.text,"html5lib")

# for k in omic_pmid:
#         print(k,omic_pmid[k])







#     print(re.split(":(?=http)",link["href"].replace("/url?q=","")))
#     searchlink = link["href"].split("/search?q=site:")
#     if len(searchlink) == 2:
        # print(searchlink[1])
        # omniclink = searchlink[1].encode("UTF-8")
        # browser.get(searchlink[1])
        # browser.execute_script("document.getElementsByClassName('content-block')[3]")
        # print(browser.page_source)
        # print(searchlink[1])
        # html = BeautifulSoup(requests.get(searchlink[1]).content,"html5lib")
        # webbody = html.find("body").prettify()
        # print(webbody)
        # pmid_class = webbody.find_all('div', attrs={"class":"content-block"})
        # print(pmid_class)
        # try:
        #     section = webbody[0]["section"]
        #     print(section)
        # except KeyError:
        #     print("section Not Found")
        # print(webcontent)

