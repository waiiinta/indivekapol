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
from selenium.webdriver.chrome.options import Options  
from random import *

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

def get_category():
        print("Crawler Start")
        response = requests.get("https://omictools.com")
        categorylink = BeautifulSoup(response.text,"html5lib")
        links = categorylink.findAll("a",{"class":"main-category-link"})
        print("Scraping")

        main_category_list = []
        # sub_category_list = []
        for link in links:
                href = link.get('href')
                # print(link.get('class'))
                if check_category_link(href):
                        if(link.get('class')[0] == 'main-category-link'):
                                main_category_list.append(href)
        print(main_category_list)
        return main_category_list

def crawl(tool_category,file,mode,count=False):
        # omic_category = ["https://omictools.com/genomics2-category",
        #                 "https://omictools.com/epigenomics-category",
        #                 "https://omictools.com/transcriptomics-category",
        #                 "https://omictools.com/proteomics-category",
        #                 "https://omictools.com/metabolomics-category",
        #                 "https://omictools.com/phenomics-category",
        #                 "https://omictools.com/text-mining-category"]

        print("Crawler Start.")
        print('count='+str(count))
        print("Crawling category start.")

        try:
                if type(tool_category) == str:
                        omic_category = open(tool_category,"r")
                else:
                        omic_category = tool_category
                subcategory_file = open(file,mode)
                category_set = set()
                for category in omic_category:
                        print("\r"+" Sending Request",end="")
                        
                        if len(category.strip().split()) > 1:
                                response = requests.get("https://omictools.com"+category.strip().split()[1])
                        else:
                                response = requests.get("https://omictools.com"+category.strip())
                        time.sleep(8)
                        categorylink = BeautifulSoup(response.text,"html5lib")
                        links = categorylink.findAll("div",{'class':'category-info'})
                        #print("\n"+category+"\n")
                        print("\r"+" Scraping "+category,end=" ")
                        if len(links) == 0:
                                category_set.add(category.strip())
                        else:
                                for link in links:
                                        href = link.find('a').get('href')
                                        if check_category_link(href):
                                                
                                                # print("-get "+href)
                                                if count == True:
                                                        num = link.find('span').getText().strip().split()[0]
                                                        category_set.add(category.strip()+" "+href+" "+num)
                                                else:
                                                        category_set.add(category.strip()+" "+href)
                        print("DONE.")
                
                for cat in category_set:
                        if mode in ["a+"]:
                                if not any(href in line for line in subcategory_file):
                                        subcategory_file.seek(0,os.SEEK_END)
                                        subcategory_file.write( cat+"\n")
                        else:
                                subcategory_file.write( cat+"\n")
                        #print(subcategory[category])
                subcategory_file.close()

        except KeyboardInterrupt:
                keyboard_interrupt_file(None,subcategory_file)
                pass

        except:
                error_found_file(None,subcategory_file)
                raise

        print("Crawling Finish.")

def list_crawl(mode):
        print("Second stage,crawling list-page of tools start.")

        try:
                subcategory_file = open("omictool_subcategory.txt","r")
                listpage_file = open("omictool_list_page.txt",mode)
                for link in subcategory_file:
                        omiclink = "https://omictools.com"+link.strip().split()[1]
                        print("\r Send Request",end="")
                        response = requests.get(omiclink)
                        sublink = BeautifulSoup(response.text,"html5lib")
                        card = sublink.findAll("article",{"class":"category-card"})
                        print("\r Scraping "+omiclink,end=" ")
                        for cate in card:
                                a = cate.find('a')
                                listpage_href = a.get('href')
                                print(listpage_href)
                                if check_category_link(listpage_href):
                                        print("Scrape "+listpage_href)
                                        listpage_file.write(link.strip().split()[0]+" "+listpage_href+"\n")
                        print("DONE.")
                        time.sleep(randint(3,6))
                listpage_file.close()
                subcategory_file.close()

        except KeyboardInterrupt:
                keyboard_interrupt_file(subcategory_file,listpage_file)
                pass

        except:
                error_found_file(subcategory_file,listpage_file)
                raise

        print("Second Stage Finish.")

def tool_crawl(mode):
        print("Third Stage,crawling paper from list page.")
        try:
                listpage_file = open("state.txt","r")
                tool_file = open("omictool_newtools.txt",mode)
                source = set()
                for listpage in listpage_file:     
                        driver = webdriver.Chrome()
                        omiclist_link = "https://omictools.com"+listpage.strip().split()[-1]
                        driver.execute_script("window.open('"+omiclist_link+"', '_blank')")
                        driver.maximize_window()
                        driver.switch_to.window(driver.window_handles[0])
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(5)
                        driver.add_cookie({
                                'name':"cookie-remember",
                                "value": '208795-%242y%2410%24vVHCEOvkPpmvzhSxdOiFlO7Tr1OuIkRWXI%2FO7Jxo0Z7QJsa5E6Rvm',
                                })
                        driver.refresh()
                        time.sleep(5)
                        html = driver.page_source
                        tab_html = BeautifulSoup(html,"html5lib")
                        page = tab_html.findAll("a",{"class":"js-page-link","href":lambda x: x and 'software' in x})
                        print(page)
                        if len(page) == 0: 
                                html = driver.page_source
                                tab_html = BeautifulSoup(html,"html5lib").find_all("div",{"class":"tool-title"})
                                for link in tab_html:
                                        tool_href = link.find('a').get('href')
                                        if check_tool_link(tool_href):
                                                if not any(tool_href == line for line in tool_file):
                                                        tool_file.seek(0,os.SEEK_END)
                                                        tool_file.write(listpage.strip()+" "+tool_href+"\n")
                                driver.quit()
                        # else:
                        #         last_page = int(page[-1].get('data-page'))
                        #         for tab in range(1,last_page):
                        #                 html = driver.page_source
                        #                 tab_html = BeautifulSoup(html,"html5lib").find_all("div",{"class":"tool-title"})
                        #                 for link in tab_html:
                        #                         tool_href = link.find('a').get('href')
                        #                         if check_tool_link(tool_href):
                        #                                 tool_file.write(tool_href+"\n")
                                        
                        #                 # button = driver.find_elements_by_xpath("//*[@id=\"tab-search-software\"]/div/section/section/section/div[2]/ul/li["+str(tab+1)+"]//a")
                        #                 # print(button)
                        #                 driver.get(omiclist_link+'?tab=software&page='+str(tab+1))
                        #                 time.sleep(5)
                                        # if tab >= 5:
                                        #         button = driver.find_elements_by_xpath("//*[@id=\"tab-search-software\"]/div/section/section/section/div[2]/ul/li["+str(5)+"]//a")
                                        # if tab == last_page-1 and last_page > 5 :
                                        #         button = driver.find_elements_by_xpath("//*[@id=\"tab-search-software\"]/div/section/section/section/div[2]/ul/li["+str(5)+"]//a") 
                                        #         webdriver.ActionChains(driver).click(button[0]).perform()
                                        #         time.sleep(3) 
                                        #         driver.switch_to.window(driver.window_handles[0])
                                        #         driver.switch_to.window(driver.window_handles[1])
                                        #         html = driver.page_source
                                        #         tab_html = BeautifulSoup(html,"html5lib").find_all("a",{"class":"tool-info-link"})
                                        #         for link in tab_html:
                                        # tool_href = link.get('href')
                                        # if check_tool_link(tool_href):
                                        #         if not any(tool_href == line for line in tool_file):
                                        #                 tool_file.seek(0,os.SEEK_END)
                                        #                 tool_file.write(tool_href+"\n")
                                        #         break
                                        # if tab == last_page-1 and last_page <= 5:
                                        #         button[0].click()
                                        #         time.sleep(3) 
                                        #         driver.switch_to.window(driver.window_handles[0])
                                        #         driver.switch_to.window(driver.window_handles[1])
                                        #         html = driver.page_source
                                        #         tab_html = BeautifulSoup(html,"html5lib").find_all("a",{"class":"tool-info-link"})
                                        #         for link in tab_html:
                                        #                 tool_href = link.get('href')
                                        #                 if check_tool_link(tool_href):
                                        #                         if not any(tool_href in line for line in tool_file):
                                        #                                 tool_file.seek(0,os.SEEK_END)
                                        #                                 tool_file.write(tool_href+"\n")
                                        #         break                                  
                                        # webdriver.ActionChains(driver).click(button[0]).perform()
                                        # time.sleep(3) 
                                        # driver.switch_to.window(driver.window_handles[0])
                                        # driver.switch_to.window(driver.window_handles[1])
                                # driver.switch_to.window(driver.window_handles[1])
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

def special_tool_crawl(mode,file):
        print("Third Stage,crawling paper from list page.")
        try:
                listpage_file = open("state.txt","r")
                tool_file = open(file,mode)
                source = set()
                for s in ['software','databases','protocols']:
                        for listpage in listpage_file:     
                                driver = webdriver.Chrome()
                                omiclist_link = "https://omictools.com"+listpage.strip().split()[-2]+'?tab'
                                driver.execute_script("window.open('"+omiclist_link+"', '_blank')")
                                driver.maximize_window()
                                driver.switch_to.window(driver.window_handles[0])
                                driver.switch_to.window(driver.window_handles[1])
                                time.sleep(5)
                                driver.add_cookie({
                                        'name':"cookie-remember",
                                        "value": '208795-%242y%2410%24vVHCEOvkPpmvzhSxdOiFlO7Tr1OuIkRWXI%2FO7Jxo0Z7QJsa5E6Rvm',
                                        })
                                driver.refresh()
                                time.sleep(5)
                                html = driver.page_source
                                tab_html = BeautifulSoup(html,"html5lib")
                                page = tab_html.findAll("a",{"class":"js-page-link","href":lambda x: x and 'software' in x})
                                print(page)
                                if len(page) == 0: 
                                        html = driver.page_source
                                        tab_html = BeautifulSoup(html,"html5lib").find_all("div",{"class":"tool-title"})
                                        for link in tab_html:
                                                tool_href = link.find('a').get('href')
                                                if check_tool_link(tool_href):
                                                        if not any(tool_href == line for line in tool_file):
                                                                tool_file.seek(0,os.SEEK_END)
                                                                tool_file.write(listpage.strip()+" "+tool_href+"\n")
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
                # r = open("./logs/pmid_state.txt","r")
                # start = r.readline()
                # r.close()
                # delete_until_found(start,"omictool_tools_rr.txt")
                print("Start crawl PMID")
                tool_file = open("omictool_toollist.txt","r")
                pmid_file = open("omictool_toollist_pmid.txt","w+")
                for t in tool_file:
                        tool = t.strip().split()[-1]
                        state = tool
                        omictool = "https://omictools.com"+tool
                        print("\r Send Request",end="")
                        response = requests.get(omictool)
                        print("\r"+" Scraping "+omictool)
                        html = BeautifulSoup(response.text,"html5lib")
                        list_of_pmid = html.find_all('div',{'class':'text'})
                        # print(list_of_pmid)
                        for pmid in list_of_pmid:
                                if pmid.text.strip()[0:4] == "PMID":
                                        print(pmid.text.strip()[6:])
                                        pmid_file.write(t.strip()+' '+pmid.text.strip()[6:]+"\n")
                        time.sleep(0.5)
                remove_redundant_tool_stage("omictool_toollist_pmid.txt")
                print("Finsh Crawl PMID")
        except KeyboardInterrupt:
                log = open("pmid_state.txt","w+")
                pmid_file.close()
                log.write(state)
                log.close()
                raise
        
        except:
                log = open("pmid_state.txt","w+")
                pmid_file.close()
                log.write(state)
                log.close()
                raise

def get_tool():
        state = ""
        try:
                r = open("./logs/pmid_state.txt","r")
                start = r.readline()
                r.close()
                delete_until_found(start,"omictool_tools_with_category.txt")
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

def all_tab_crawl(mode,file):
        print("Third Stage,crawling paper from list page.")
        try:
                listpage_file = open("state.txt","r")
                tool_file = open(file,mode)
                source = set()
                for listpage in listpage_file:  
                        driver = webdriver.Chrome()
                        omiclist_link = "https://omictools.com"+listpage.strip().split()[-2]
                        driver.execute_script("window.open('"+omiclist_link+"', '_blank')")
                        driver.maximize_window()
                        driver.switch_to.window(driver.window_handles[0])
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(5)
                        driver.add_cookie({
                                'name':"cookie-remember",
                                "value": '208795-%242y%2410%24vVHCEOvkPpmvzhSxdOiFlO7Tr1OuIkRWXI%2FO7Jxo0Z7QJsa5E6Rvm',
                                })
                        driver.refresh()
                        time.sleep(5)
                        # print(page)
                        html = driver.page_source  
                        html = BeautifulSoup(html,"html5lib")
                                
                        tabs = html.findAll("a",{"data-tab":lambda x: x in ['software','databases','protocols']})    
                        tabs_list = [i.get('data-tab') for i in tabs]
                        
                        for s in tabs_list:
                                omiclist_link = "https://omictools.com"+listpage.strip().split()[-2]+'?tab='+s
                                driver.get(omiclist_link)
                                time.sleep(5)
                                # print(page)
                                html = driver.page_source
                                if s in ['software','databases']:        
                                        tab_html = BeautifulSoup(html,"html5lib").find_all("div",{"class":"tool-title"})
                                        for link in tab_html:
                                                tool_href = link.find('a').get('href')
                                                if check_tool_link(tool_href):
                                                        if not any(tool_href == line for line in tool_file):
                                                                tool_file.seek(0,os.SEEK_END)
                                                                tool_file.write(listpage.strip()+" "+tool_href+"\n")
                                # else:
                                #         tab_html = BeautifulSoup(html,"html5lib").find_all("a",{"class":'corpus-title'})
                                #         for link in tab_html:
                                #                 print(link)
                                #                 tool_href = link.get('href')
                                #                 if check_tool_link(tool_href):
                                #                         if not any(tool_href == line for line in tool_file):
                                #                                 tool_file.seek(0,os.SEEK_END)
                                #                                 tool_file.write(listpage.strip()+" "+tool_href+"\n")
                                time.sleep(10)
                        driver.quit()
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

def main():
        # omic_category = ["https://omictools.com/genomics2-category",
        #                 "https://omictools.com/epigenomics-category",
        #                 "https://omictools.com/transcriptomics-category",
        #                 "https://omictools.com/proteomics-category",
        #                 "https://omictools.com/metabolomics-category",
        #                 "https://omictools.com/phenomics-category"]
        # category_list = get_category()
        # crawl(category_list,"omictool_maincategory.txt","w",count=True)
        # crawl("omictool_maincategory.txt","omictool_subcategory.txt","w+",count=True)
        # all_tab_crawl('a+','omictool_toollist.txt')
        # tool_crawl("a+")
        get_tool_pmid()
        # remove_redundant_tool_stage("omictool_pmid.txt")
                
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








