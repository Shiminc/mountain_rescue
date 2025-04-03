from bs4 import BeautifulSoup
import requests

url = "https://www.wmrt.org.uk/incidents/page/"

def main():
    pages = 130
    case_links = []

    for page in range(1,pages+1):
        print(f'processing page {page}')
        url_page = f'{url}{page}'
        page_content = requests.get(url_page)
        soup = BeautifulSoup(page_content.text, 'html.parser')
        titles = soup.find_all("h2", "card-title entry-title")

        for title in titles:
            case_links.append(title.find_all('a')[0]['href'])
    
    case_links_linebreak = [x + '\n' for x in case_links]
    with open('case_links.txt','w') as file:
        file.writelines(case_links_linebreak)
        
    return

main()