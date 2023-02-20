from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
import time

x = 1
all_data = []
counter = 1
unique_jobs = []

while True:

    html_code = requests.get('https://jobs.gamedeveloper.com/jobs/?&p='+str(x))
    logging.info(f"Extracting data from page {x}")
    html_code = html_code.text

    soup = BeautifulSoup(html_code, 'html.parser')
    jobs = soup.find_all("div", class_="listing-item-center")
    logging.info(f"Total {len(jobs) - len(unique_jobs)} records found.")
    for job in jobs:
        if job not in unique_jobs:
            data = {}
            try:
                data["title"] = job.find_all("a")[0].text
            except:
                data['title'] = None
            try:
                data['url'] = job.find_all("a")[0]['href']
            except:
                data['url'] = None
            try:
                data["company_name"] = job.find("div", class_="listing-item__additional listing-item__additional--company").text.strip()
            except:
                data['company_name'] = None
            try:
                data["location"] = job.find("div", class_="listing-item__additional listing-item__additional--location").text.strip()
            except:
                data['location'] = None
            try:
                data["posting_date"] = job.find("div", class_="listing-item__additional listing-item__additional--date").text.strip()
            except:
                data['posting_date'] = None
            serial_number = data['url'].split("/")[4]
            data["link_to_apply"] = "https://jobs.gamedeveloper.com/application-redirect/?listing_id=" + serial_number
            job_page = requests.get('https://jobs.gamedeveloper.com/job/' + str(serial_number), headers = {'User-agent': 'your bot 0.1'})
            page_soup = BeautifulSoup(job_page.text, 'html.parser')
            try:
                data["job_type"] = page_soup.find("div", class_="job-type").text.strip()
            except:
                data['job_type'] = None
            try:
                data["job_description"] = page_soup.find("div", class_="row details-body").text.strip()
            except:
                data['job_description'] = None
            try:
                data["salary"] = page_soup.find("li", class_="listing-item__info--item listing-item__info--item-salary-range").text.strip()
            except:
                data['salary'] = "Not defined"
            logging.info(f"Record number : {counter} - Successfully Scrapped data for {data['title']}")
            counter += 1
            all_data.append(data)
            results = pd.DataFrame(all_data)
            results = results.to_csv("game_developer_data.csv", index=False) 
            unique_jobs.append(job)
    x += 1
    if len(jobs) == 0:
        break

        
        
        
        
        
    
     
