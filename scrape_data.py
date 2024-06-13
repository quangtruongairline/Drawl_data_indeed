
import argparse
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from utils import save_data, access, info_job,search, init_driver

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default= "https://vn.indeed.com/jobs")
    parser.add_argument("--job", default="AI, Data Science")
    parser.add_argument("--location", default="Thành Phố Hồ Chí Minh")
    args = parser.parse_args()
    
    
    driver=init_driver()
    
    url, job_, location = args.url, args.job, args.location
    
    access(driver,url)
    
    search(driver,job_,location)
    data=info_job(driver)
    save_data(data)
    
    
    