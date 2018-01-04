# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import json
import shutil

shutil.rmtree('output', ignore_errors=True)
os.mkdir('output')
os.chdir('output')
d = []
for i in range(2, 19):
    r = requests.get('http://www.lcsd.gov.hk/tc/facilities/facilitieslist/facilities.php?ftid=38&did=%d' % (i))
    r.encoding='utf-8'
    soup = BeautifulSoup(r.content, "html.parser", from_encoding=r.encoding)
    selected = soup.find_all('option', selected=True)
    if len(selected) == 0:
        continue
    selected = selected[0]
    district = selected.text.replace("-", "").strip()
    district_dir_name = str(i)
    os.mkdir(district_dir_name)
    os.chdir(district_dir_name)

    headers = soup.find_all('h2')
    tables = soup.find_all('table')
    schedules = []
    for table in tables:
        rows = table.find_all('tr')
        if len(rows) == 1:
            links = rows[0].find_all('a')
            for link in links:
                if 'pdf' in link['href']:
                    schedules.append([l['href'] for l in links])
                    break

    places = []
    for header, schedule in zip(headers, schedules):
        if len(schedule) > 0:
            first_pdf_url = schedule[0]
            segments = first_pdf_url.split('/')
            key = int(segments[3].split('_')[0])
            dir_name = str(key)
            print(dir_name)
            os.mkdir(dir_name)
            os.chdir(dir_name)
            for pdf in schedule:
                pdf_url = 'http://www.lcsd.gov.hk' + pdf
                os.system('wget ' + pdf_url)
            os.chdir('..')
            places.append({'name': header.text, 'id': key})
    d.append({'district': district, 'places': places})
    os.chdir('..')

with open('mapping.json', 'w') as f:
    f.write(json.dumps(d, indent=4))
