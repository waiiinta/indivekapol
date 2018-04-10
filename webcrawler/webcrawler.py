from urllib.request import urlopen,Request 
from bs4 import BeautifulSoup 
import requests
import re
import time
from pathlib import Path
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def check_category_link(link):
        if link != None and \
                len(link) > 8 and \
                link[len(link)-8:len(link)] == "category" and \
                link[0] == "/":
                return True
        else:
                return False

def check_tool_link(link):
        if len(link) > 8 and \
                link[len(link)-4:len(link)] == "tool" and \
                link[0] == "/":
                return True
        else:
                return False

def keyboard_interrupt_file(r_file,w_file):
        print('\n'+"Program get interrupt")
        w_file.close()
        if r_file != None:
                r_file.close()
        print("Pass the stage")

def error_found_file(r_file,w_file):
        print('\n'+'ERROR FOUND!')
        w_file.close()
        if r_file != None:
                r_file.close()

def remove_redundancy(r_file):
        new_set = set()
        for line in r_file:
                new_set.add(line.strip())
        return new_set

def first_crawl():
        omic_category = ["https://omictools.com/genomics2-category",
                        "https://omictools.com/epigenomics-category",
                        "https://omictools.com/transcriptomics-category",
                        "https://omictools.com/proteomics-category",
                        "https://omictools.com/metabolomics-category",
                        "https://omictools.com/phenomics-category",
                        "https://omictools.com/text-mining-category"]

        print("Crawler Start.")
        print("First Stage,Crawling subcategory start.")

        try:
                subcategory_file = open("omictool_subcategory.txt","a+")
                for category in omic_category:
                        print("\r"+" Sending Request",end="")
                        response = requests.get(category)
                        categorylink = BeautifulSoup(response.text,"html5lib")
                        links = categorylink.findAll("a")
                        #print("\n"+category+"\n")
                        print("\r"+" Scraping "+category,end=" ")
                        for link in links:
                                href = link.get('href')
                                if check_category_link(href):
                                        if not any(href in line for line in subcategory_file):
                                                subcategory_file.seek(0,os.SEEK_END)
                                                subcategory_file.write( href+"\n")
                        print("DONE.")
                        time.sleep(5)
                        #print(subcategory[category])
                subcategory_file.close()

        except KeyboardInterrupt:
                keyboard_interrupt_file(None,subcategory_file)
                pass

        except:
                error_found_file(None,subcategory_file)
                raise

        print("Crawling First Stage Finish.")

def second_crawl():
        print("Second stage,crawling list-page of tools start.")

        try:
                subcategory_file = open("omictool_subcategory.txt","r")
                listpage_file = open("omictool_list_page.txt","a+")
                for link in subcategory_file:
                        omiclink = "https://omictools.com"+link.strip()
                        print("\r Send Request",end="")
                        response = requests.get(omiclink)
                        sublink = BeautifulSoup(response.text,"html5lib")
                        card = sublink.findAll("article",{"class":"category-card"})
                        print("\r Scraping "+omiclink,end=" ")
                        for cate in card:
                                a = cate.find('a')
                                listpage_href = a.get('href')
                                if check_category_link(listpage_href):
                                        if not any(listpage_href == line for line in listpage_file):
                                                listpage_file.seek(0,os.SEEK_END) 
                                                listpage_file.write(listpage_href+"\n")
                        print("DONE.")
                        time.sleep(3)
                listpage_file.close()
                subcategory_file.close()

        except KeyboardInterrupt:
                keyboard_interrupt_file(subcategory_file,listpage_file)
                pass

        except:
                error_found_file(subcategory_file,listpage_file)
                raise

        print("Second Stage Finish.")
        print("Third Stage,crawling paper from list page.")

def tool_crawl():
        try:
                listpage_file = open("omictool_list_page.txt","r")
                tool_file = open("omictool_tools.txt","a+")
                source = set()
                for listpage in listpage_file:     
                        driver = webdriver.Chrome()
                        omiclist_link = "https://omictools.com"+listpage.strip()
                        driver.execute_script("window.open('"+omiclist_link+"', '_blank')")
                        driver.maximize_window()
                        driver.switch_to.window(driver.window_handles[0])
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(5)
                        html = driver.page_source
                        tab_html = BeautifulSoup(html,"html5lib")
                        page = tab_html.findAll("a",{"class":"js-page-link"})
                        if len(page) == 0: 
                                html = driver.page_source
                                tab_html = BeautifulSoup(html,"html5lib").find_all("a",{"class":"tool-info-link"})
                                for link in tab_html:
                                        tool_href = link.get('href')
                                        if check_tool_link(tool_href):
                                                if not any(tool_href == line for line in tool_file):
                                                        tool_file.seek(0,os.SEEK_END)
                                                        tool_file.write(tool_href+"\n")
                                driver.quit()
                        else:
                                last_page = int(tab_html.findAll("a",{"class":"js-page-link"})[-1].get('data-page'))
                                for tab in range(1,last_page):
                                        html = driver.page_source
                                        tab_html = BeautifulSoup(html,"html5lib").find_all("a",{"class":"tool-info-link"})
                                        for link in tab_html:
                                                tool_href = link.get('href')
                                                if check_tool_link(tool_href):
                                                        tool_file.write(tool_href+"\n")
                                        
                                        button = driver.find_elements_by_xpath("//html//body//div[2]//main//section//div[2]//div[2]//ul//li["+str(tab+1)+"]//a")
                                        time.sleep(5)
                                        if tab >= 5:
                                                button = driver.find_elements_by_xpath("//html//body//div[2]//main//section//div[2]//div[2]//ul//li["+str(5)+"]//a")
                                        if tab == last_page-1 and last_page > 5 :
                                                button = driver.find_elements_by_xpath("//html//body//div[2]//main//section//div[2]//div[2]//ul//li["+str(5)+"]//a") 
                                                webdriver.ActionChains(driver).click(button[0]).perform()
                                                time.sleep(3) 
                                                driver.switch_to.window(driver.window_handles[0])
                                                driver.switch_to.window(driver.window_handles[1])
                                                html = driver.page_source
                                                tab_html = BeautifulSoup(html,"html5lib").find_all("a",{"class":"tool-info-link"})
                                                for link in tab_html:
                                                        tool_href = link.get('href')
                                                        if check_tool_link(tool_href):
                                                                if not any(tool_href == line for line in tool_file):
                                                                        tool_file.seek(0,os.SEEK_END)
                                                                        tool_file.write(tool_href+"\n")
                                                break
                                        if tab == last_page-1 and last_page <= 5:
                                                webdriver.ActionChains(driver).click(button[0]).perform()
                                                time.sleep(3) 
                                                driver.switch_to.window(driver.window_handles[0])
                                                driver.switch_to.window(driver.window_handles[1])
                                                html = driver.page_source
                                                tab_html = BeautifulSoup(html,"html5lib").find_all("a",{"class":"tool-info-link"})
                                                for link in tab_html:
                                                        tool_href = link.get('href')
                                                        if check_tool_link(tool_href):
                                                                if not any(tool_href in line for line in tool_file):
                                                                        tool_file.seek(0,os.SEEK_END)
                                                                        tool_file.write(tool_href+"\n")
                                                break                                  
                                        webdriver.ActionChains(driver).click(button[0]).perform()
                                        time.sleep(3) 
                                        driver.switch_to.window(driver.window_handles[0])
                                        driver.switch_to.window(driver.window_handles[1])
                                driver.switch_to.window(driver.window_handles[1])
                                driver.quit()
                                time.sleep(10)
                tool_file.close()
                listpage_file.close()
                                
        except KeyboardInterrupt:
                print("Program get interrupted")
                tool_file.close()
                listpage_file.close()
                print("Pass Third Stage")
                pass
        except:
                print('\n'+'ERROR FOUND!')
                tool_file.close()
                listpage_file.close()
                raise

        print("Crawl tool Finish.")

def remove_redundant_tool_stage(file):
        print("Remove redundancy from file.")

        try:
                tool_file = open(file,"r")
                rr_tool_set = sorted(remove_redundancy(tool_file))
                tool_file.close()
                rr_tool_file = open(file,"w+")
                for tool in rr_tool_set:
                        if not any(tool in line for line in rr_tool_file):
                                rr_tool_file.seek(0,os.SEEK_END)
                                rr_tool_file.write(tool+'\n')
                print("Number of tool after remove redundancy : " + str(len(rr_tool_set)))
                tool_file.close()
                rr_tool_file.close()

        except KeyboardInterrupt:
                keyboard_interrupt_file(tool_file,rr_tool_file)
                pass

        except:
                error_found_file(tool_file,rr_tool_file)
                raise

        print("Third Stage Finish.")

def delete_until_found(name,file):
        print("Update "+file)
        r_file = open(file,"r")
        tool_text = r_file.readlines()
        start = tool_text.index(name)
        after_delete_text = tool_text[start:]
        r_file.close()
        w_file = open(file,"w")
        for tool_name in after_delete_text:
                w_file.write(tool_name)
        print("Now "+file+", First line is "+after_delete_text[0])
        w_file.close()
        time.sleep(1.5)

def get_tool_pmid():
        state = ""
        try:
                r = open("./logs/pmid_state.txt","r")
                start = r.readline()
                r.close()
                delete_until_found(start,"omictool_tools_rr.txt")
                print("Start crawl PMID")
                tool_file = open("omictool_tools_rr.txt","r")
                pmid_file = open("omictool_pmid.txt","a+")
                for tool in tool_file:
                        state = tool
                        omictool = "https://omictools.com"+tool.strip()
                        print("\r Send Request",end="")
                        response = requests.get(omictool)
                        print("\r"+" Scraping "+omictool)
                        html = BeautifulSoup(response.text,"html5lib")
                        list_of_pmid = html.find_all('span')
                        for pmid in list_of_pmid:
                                if pmid.text[0:4] == "PMID":
                                        print(pmid.text)
                                        pmid_file.write(pmid.text[6:]+"\n")
                        time.sleep(0.5)
                remove_redundant_tool_stage("omictool_pmid.txt")
                print("Finsh Crawl PMID")
        except:
                log = open("./logs/pmid_state.txt","w+")
                log.write(state)
                log.close()
                raise

def main():
        remove_redundant_tool_stage("omictool_pmid.txt")
                
main()



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








