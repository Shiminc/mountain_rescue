from bs4 import BeautifulSoup
import requests, re
from datetime import datetime


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
    texts = soup.find_all('p')

    # find the boundary p which is space only that separate main text and info text
    x = [p.get_text()=='\xa0' for p in texts]
    if True in x:
        boundary = x.index(True)

        main_text = ""
        for i in range(1,boundary):
            main_text = main_text + texts[i].get_text() + ' '

        info_text = texts[boundary + 1].get_text()
    else:
        main_text = texts[1].get_text()
        info_text = texts[2].get_text()
    
    return main_text, info_text

def extract_info_from_text(table):
    matches = re.search(r"started at ([0-9]{2}:[0-9]{2})", table['info_text']) 
    if matches:
        table['start_time'] = matches.group(1)
    matches = re.search(r"ended at ([0-9]{2}:[0-9]{2})", table['info_text']) 
    if matches:
        table['end_time'] = matches.group(1)
    matches = re.search(r"(\d+\.?\d*) hrs", table['info_text'])
    if matches:
        table['hrs'] = matches.group(1)
    matches = re.search(r"(\d+) Wasdale", table['info_text']) 
    if matches:
        table['staff'] = matches.group(1)
    matches = re.search(r"(NY[ \d]+)", table['info_text']) 
    if matches:
        table['location'] = matches.group(1)
    matches = re.search(r"Total rescuer hours: (\d+\.?\d*)", table['info_text'])
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
    main_text, info_text = extract_text(soup)
    table['main_text'] = main_text
    table['info_text'] = info_text
    table_info = extract_info_from_text(table)
    final_table = format_date_time(table_info)
    return final_table

def main():
    urls = load_links()
    data = []
    for i in range(0,20):
        url = urls[i][:-1]
        print(f'scraping {url}')
        data.append(scrape_one_incident(url))
    #trial = scrape_one_incident(url)
    with open('twenty_incidents.json','w') as file:
        file.writelines(data) 
    print('finish!')

main()