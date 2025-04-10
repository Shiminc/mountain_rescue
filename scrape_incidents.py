from bs4 import BeautifulSoup
import requests, re
from datetime import datetime
import json


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
    main_text = ""

    ## there are difference occassions the text is presented

    # condition 1: main text is not in p tag 
    if soup.find_all('div', dir = 'auto'):
        for text in soup.find_all('div', dir = 'auto'):
            if text.get_text() == 'https://www.adventuresmart.uk/':
                break
            else:
                main_text = main_text + text.get_text() + ' '


    else: # condition 2 (main and info text are in p and separate by an empty p tag) and condition 3 (no empty p tag)
        texts = soup.find_all('p')
        
        for p in texts:
                if p.get_text().startswith(' Incident started'):
                    break
                elif p.get_text()=='\xa0':
                    break
                elif p.get_text().startswith('#BeAdventureSmart'):
                    break
                else:
                    main_text = main_text + p.get_text() + ' '

    main_text = main_text.removeprefix('Wasdale Mountain Rescue ')

    return main_text

def extract_rescue_info(soup):
    if soup.find('div', id = 'rescueinfo'):
        rescue_info = soup.find('div', id = 'rescueinfo').get_text()
    else:
        rescue_info = ''
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
    #final_table = format_date_time(table_info) # does not work for json dump
    #return final_table
    return table_info

def main():
    urls = load_links()
    data = []
    for i in range(0,len(urls)):
        url = urls[i][:-1] # to drop the \n in each line
        print(f'scraping {url}')
        data.append(scrape_one_incident(url))

    with open('all_incidents.json','w') as file:
        json.dump(data,file)
    print('finish!')

main()