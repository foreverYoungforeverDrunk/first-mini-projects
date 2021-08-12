from bs4 import BeautifulSoup
import requests
import json
import re

headers = {'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,be;q=0.6'}
regexp = r'\d{4}'


def get_html(url):
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    imdb = soup.find('tbody', class_='lister-list')
    imdb250 = imdb.find_all('tr')

    results = []

    for item in imdb250:
        place = item.find('td', class_='titleColumn').next.strip()
        names = item.find('a').next_element.next_element
        name = names.get('alt')
        year = item.find(text=re.compile(regexp))
        rank = item.find('strong').next
        # print(rank)
        results.append({
            'place': place,
            'name': name,
            'year': year,
            'rank': rank
        })
    return results


def write_json(results):
    with open('imdb250function.json', 'w') as file:
        json.dump(results, file, indent=2)


def main():
    url = f'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    html = get_html(url)
    results = get_all_links(html)
    write_json(results)


if __name__ == '__main__':
    main()
