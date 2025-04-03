from bs4 import BeautifulSoup
import requests

url = 'https://www.wmrt.org.uk/incidents/corridor-route-scafell-pike-tue-18th-feb-2025/'


def main():
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.text, 'html.parser')
    date = soup.find('h1').get_text()
    table = soup.find('dl','dl-horizontal')
    rescue_info = soup.find(id="rescueinfo")


    print('finish!')

main()