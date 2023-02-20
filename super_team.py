import requests
import pandas as pd
import time
import json
from bs4 import BeautifulSoup
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

new_data = []
counter = 1
urls = ["https://earn.superteamearn.workers.dev/?key=jobs", "https://earn.superteamearn.workers.dev/?key=bounties"]
for url in urls:

    querystring = {"key":"jobs, bounties"}

    headers = {
        "authority": "earn.superteamearn.workers.dev",
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://earn.superteam.fun",
        "referer": "https://earn.superteam.fun/",
        "sec-ch-ua": "^\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    all_data = data['data']['value']
    all_data = json.loads(all_data)
    for data in all_data:
        if "workable" in data['Application Link']:
            try:
                description_page = requests.get("https://apply.workable.com/api/v2/accounts/aldrin/jobs/" + data['Application Link'].split("/")[-1])
            except:
                continue
        else:
            try:
                description_page = requests.get(data['Application Link'])
            except:
                continue
        logging.info(f"Getting job number {counter} : {data['Opportunity Title']}")
        counter += 1
        page_soup = BeautifulSoup(description_page.text, 'html.parser')
        data['job_description'] = page_soup.text
        new_data.append(data)
        results = pd.DataFrame(new_data)
        try:
            results = results.drop(["objectID", "Sponsor (Linked from Sponsors Table)", "Skills Needed", "externalId", "Removed Sponsor", "Sponsor (text field)", "Industry", "sponsorTwitter",], axis=1)
        except:
            continue
        result = results.to_csv("super_team.csv", index=False)