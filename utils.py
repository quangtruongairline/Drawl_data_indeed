import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
# import pandas as pd
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import datetime
import json
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options



#______________________________
def init_driver():
    
    # edge_options = webdriver.EdgeOptions()
    # options = Options()
    # driver = webdriver.Edge(options=edge_options)
    # cService = webdriver.ChromeService(executable_path='./chromedriver.exe')
    # driver = webdriver.Chrome(service = cService)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver


#____________________________________________

def access(driver,url):
    print("_"*30, "ACCESS URL","_"*30)
    driver.get(url)
    sleep(3)


def search(driver, job, location):
    print("_"*30, "SEARCH","_"*30)
    search_box_job = driver.find_element(By.XPATH, '//input[@id="text-input-what"]')#(By.ID, 'text-input-what')
    search_box_location=driver.find_element(By.XPATH, '//input[@id="text-input-where"]')#(By.ID, 'text-input-where')
    search_box_job.send_keys(job)
    search_box_location.send_keys(location)

    search_box_location.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    
    next = driver.find_element(By.XPATH, '//a[@data-testid="pagination-page-next"]')
    next.click()
    sleep(4)


def save_data(dict_jd):
    directory = './'
    
    today = str(datetime.date.today())
    filename = f"{directory}/data_{today}.json"
    
    
    json_file = json.dumps(dict_jd, indent= 4, ensure_ascii=False)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json_file)
    

def info_job(driver):
    
    id=0

    num_job= driver.find_element(By.XPATH, '//div[@class="jobsearch-JobCountAndSortPane-jobCount css-13jafh6 eu4oa1w0"]//span').text
    num_job_=re.sub(r'\D', '', num_job)
    num_job=int(num_job_)
    num_next= num_job//15

    if num_next >15 :
        num_next=15
        
    dict_job={}
    for i in range(0,num_next-2):
        info_jobs = driver.find_elements(By.XPATH, '//div[@class="job_seen_beacon"]')
        print("_"*30, "START","_"*30)
        
        
        try:
            close = driver.find_element(By.XPATH, '//button[@aria-label="close"]')
            close.click()
        except NoSuchElementException:
            pass
        
        for element in info_jobs:
            
            element.click()     
            try:              
                name_job_ = driver.find_element(By.XPATH, '//h2[@data-testid="jobsearch-JobInfoHeader-title"]/span').text
                name_job = name_job_.replace("- job post", "").strip()
                            
                name_company = driver.find_element(By.XPATH, '//div[@data-testid="inlineHeader-companyName"]/span/a').text

                location = driver.find_element(By.XPATH, '//div[@data-testid="inlineHeader-companyLocation"]/div').text
                
        
                job_description = driver.find_elements(By.XPATH, '//div[@id="jobDescriptionText"]')

                content_jd = ""
                for jd in job_description:
                    get_html = jd.get_attribute("innerHTML")             
                    parser = BeautifulSoup(get_html, 'html.parser')        
                    jd = parser.get_text()    
                    content_jd += jd.replace("\n"," ").replace("   ","")
                id+=1
                
                try:
                    dict_job[id]
                except KeyError:
                    dict_job[id] = {
                        "ID":id,
                        "job":name_job,
                        "company": name_company,
                        "location": location,
                        "job_description":content_jd  
                    }
                
                sleep(4)
            except NoSuchElementException:
                pass
        
        next = driver.find_element(By.XPATH, '//a[@data-testid="pagination-page-next"]')
        next.click()
        sleep(4)
        
        try:
            close = driver.find_element(By.XPATH, '//button[@aria-label="close"]')
            close.click()
        except NoSuchElementException:
            pass
    
    driver.quit() 
    return dict_job
        

