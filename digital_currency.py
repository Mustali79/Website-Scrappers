from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)


x = 1
all_data = []
counter = 1
unique_jobs = []

while True:

    html_code = requests.get('https://jobs.dcg.co/jobs?page='+str(x))
    logging.info(f"Extracting data from page {x}")
    html_code = html_code.text

    soup = BeautifulSoup(html_code, 'html.parser')
    jobs = soup.find_all("div", class_="sc-AxjAm fWoBxm job-card")
    if len(unique_jobs) >= len(jobs):
        break
    logging.info(f"Total {len(jobs) - len(unique_jobs)} records found.")
    for job in jobs:
        if job not in unique_jobs:
            data = {}
            try:
                data["title"] = job.find("div", class_="sc-AxjAm fQfMRj").text
            except:
                data['title'] = None
            try:
                data['url'] = job.find_all("a")[1]['href']
            except:
                data['url'] = None
            try:
                job_page = requests.get(data['url'])
                page_soup = BeautifulSoup(job_page.text, 'html.parser')
                data['job_description'] = page_soup.text
            except:
                data['job_description'] = None
            try:
                data["company_name"] = job.find("div", class_="sc-AxjAm oDrAC").find("a").text.strip()
            except:
                data['company_name'] = None
            try:
                data['location'] = job.find("div", class_="sc-AxjAm sc-AxirZ hVyOBs").text.strip()
            except:
                data['location'] = "None"
            if data['location'] != None and "Remote" in data['location']:
                    data['is_remote'] = "Yes"
                    data['location'] = data['location'].replace("Remote", "") 
            else:
                data['is_remote'] = "No"
            try:
                 data["posting_date"] = job.find("div", class_="sc-AxjAm sc-AxirZ cvSyfg added").text.strip()
            except:
                 data['posting_date'] = None
            logging.info(f"Record number : {counter} - Successfully Scrapped data for {data['title']}")
            counter += 1
            all_data.append(data)
            results = pd.DataFrame(all_data)
            results = results.to_csv("digital_currency.csv", index=False) 
            unique_jobs.append(job)
    x += 1
    