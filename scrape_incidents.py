from bs4 import BeautifulSoup
import requests, re
from datetime import datetime
import json

url = 'https://www.wmrt.org.uk/incidents/corridor-route-scafell-pike-tue-18th-feb-2025/'

def create_soup(url):
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.text, 'html.parser')
    return soup

def extract_table(soup):
    title = soup.find('h1').get_text()
    table_dict = {'title':title}

    #extract date
    matches = re.search(r"([0-9]{1,2})(?:st|nd|rd|th) ([a-zA-Z]{3} [0-9]{4})", title)
    if matches:
        date = matches.group(1) + ' ' +  matches.group(2)
        table_dict['date'] = date

    table = soup.find('dl','dl-horizontal')
    headings = table.find_all('dt')
    details = table.find_all('dd')

    for i in range(0,len(headings)):
        table_dict[headings[i].string] = details[i].get_text().replace('\xa0', ' ')
    
    # processing the table content
    if 'Type' in table_dict.keys():
        incident = table_dict['Type'].split(' — ')
        table_dict['Incident_Type'] = incident[0]
        table_dict['Incident_Cause'] = incident[1]

    if 'Weather' in table_dict.keys():
        table_dict['Weather'] = table_dict['Weather'].split(', ')

    if 'Tagged' in table_dict.keys():
        table_dict['Tagged'] = table_dict['Tagged'].split(', ')
    
    if 'Other Agencies' in table_dict.keys():
        table_dict['Other Agencies'] = table_dict['Other Agencies'].split(', ')

    return table_dict

def extract_text(soup):
    ## there are difference occassions the text is presented

    # condition 1: main text is not in p tag, while info text is 
    if soup.find_all('div', dir = 'auto'):
        for text in soup.find_all('div', dir = 'auto'):
            if text.get_text() == 'https://www.adventuresmart.uk/':
                break
            else:
                main_text = text.get_text()


    else: # condition 2 (main and info text are in p and separate by an empty p tag) and condition 3 (no empty p tag)
        texts = soup.find_all('p')
        
        # find the boundary p which is space only that separate main text and info text
        x = [p.get_text()=='\xa0' for p in texts]
        if True in x: #condition 2
            boundary = x.index(True)

            main_text = ""
            for i in range(1,boundary):
                main_text = main_text + texts[i].get_text() + ' '

        else: #condition 3
            main_text = texts[1].get_text()
    
    return main_text

def extract_rescue_info(soup):
    rescue_info = soup.find('div', id = 'rescueinfo').get_text()
    return rescue_info

def extract_rescue_info_from_text(table):
    matches = re.search(r"started at ([0-9]{2}:[0-9]{2})", table['rescue_info']) 
    if matches:
        table['start_time'] = matches.group(1)
    matches = re.search(r"ended at ([0-9]{2}:[0-9]{2})", table['rescue_info']) 
    if matches:
        table['end_time'] = matches.group(1)
    matches = re.search(r"(\d+\.?\d*) hrs", table['rescue_info'])
    if matches:
        table['hrs'] = matches.group(1)
    matches = re.search(r"(\d+) Wasdale", table['rescue_info']) 
    if matches:
        table['staff'] = matches.group(1)
    matches = re.search(r"(NY[ \d]+)", table['rescue_info']) 
    if matches:
        table['location'] = matches.group(1)
    matches = re.search(r"Total rescuer hours: (\d+\.?\d*)", table['rescue_info'])
    if matches:
        table['total_hrs'] = matches.group(1)
    
    return table

def format_date_time(table_dict):
    table_dict['date_obj'] = datetime.strptime(table_dict['date'], "%d %b %Y")
    start_time = table_dict['date'] + ' ' + table_dict['start_time']
    table_dict['start_time_obj'] = datetime.strptime(start_time, "%d %b %Y %H:%M")
    end_time = table_dict['date'] + ' ' + table_dict['end_time']
    table_dict['end_time_obj'] = datetime.strptime(end_time, "%d %b %Y %H:%M")
    return table_dict

def load_links():
    with open('case_links.txt','r') as file:
        links = file.readlines()
    return links

def scrape_one_incident(url):
    soup = create_soup(url)
    table = extract_table(soup)
    table['url'] = url
    table['main_text'] = extract_text(soup)
    table['rescue_info'] = extract_rescue_info(soup)
    table_info = extract_rescue_info_from_text(table)
    #final_table = format_date_time(table_info)
    #return final_table
    return table_info

def main():
    urls = load_links()
    data = []
    for i in range(0,20):
        url = urls[i][:-1]
        print(f'scraping {url}')
        data.append(scrape_one_incident(url))
    #url = 'https://www.wmrt.org.uk/incidents/upper-eskdale-sat-22nd-mar-2025/'
        #trial = scrape_one_incident(url)
    with open('twenty_incidents.json','w') as file:
        json.dump(data,file)
    print('finish!')

main()