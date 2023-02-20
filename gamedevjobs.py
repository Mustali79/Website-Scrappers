from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)


x = 1
all_data = []
unique_jobs = []
counter = 1

while True:

    html_code = requests.get('https://gamedevjobs.com/page/'+str(x))
    logging.info(f"Extracting data from page {x}")
    html_code = html_code.text

    soup = BeautifulSoup(html_code, 'html.parser')
    jobs = soup.find_all("div", class_="css-1qeu6k4")
    logging.info(f"Total {len(jobs)} records found.")
    for job in jobs:
        if job not in unique_jobs:
            unique_jobs.append(job)
            data = {}
            try:
                data['url'] ="https://gamedevjobs.com" + job.find("a")['href']
            except:
                data['url'] = None
            job_page = requests.get(data['url'])
            page_soup = BeautifulSoup(job_page.text, 'html.parser')
            try:
                data["title"] = job.find("a").text.strip()
            except:
                data['title'] = None
            try:
                data["company_name"] = job.find("p", class_="chakra-text css-0").text.strip()
            except:
                data['company_name'] = None
            try:
                data['link_to_apply'] = page_soup.find("div", class_="css-15cp6fo").find("a")['href']
            except:
                data['link_to_apply'] = None
            try:
                data["location"] = page_soup.find("div", class_="css-1ayfwcb").find_all("p")[0].text.strip().split(":")[1].strip()
                if ">" in data['location']:
                    data['location'] = "None"
            except:
                data['location'] = None
            try:
                data['country'] = page_soup.find("div", class_="css-1ayfwcb").find_all("p")[1].text.strip().split(":")[1].strip()
            except:
                data['country'] = None
            try:
                data['posting_date'] = page_soup.find('span', {'itemprop':'datePosted'}).text
                
            except:
                data['posting_date'] = None
            try:
                data["job_description"] = page_soup.find("div", class_="Job_job_description__TL45y css-wn8rfm").text.strip()
            except:
                data['job_description'] = None
            logging.info(f"Record number : {counter} - Successfully Scrapped data for {data['title']}")
            counter += 1
            all_data.append(data)
            results = pd.DataFrame(all_data)
            results = results.to_csv("game_dev_jobs.csv", index=False) 
    x += 1
    if len(jobs) == 0:
        break