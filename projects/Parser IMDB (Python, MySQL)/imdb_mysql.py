from bs4 import BeautifulSoup
import requests
import re
from contextlib import closing
import pymysql
from pymysql.cursors import DictCursor
from environs import Env

env = Env()
env.read_env("mysql.env")

user = env.str("user")
password = env.str("password")


def get_html(url):
    headers = {'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,be;q=0.6'}
    r = requests.get(url, headers=headers)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    imdb = soup.find('tbody', class_='lister-list')
    imdb250 = imdb.find_all('tr')

    results = []
    regexp = r'\d{4}'

    for item in imdb250:
        names = item.find('a').next_element.next_element
        title = names.get('alt')
        release_year = item.find(text=re.compile(regexp)).strip()
        rank_films = item.find('strong').next
        results.append({
            'title': title,
            'release_year': release_year,
            'rank_films': rank_films
        })
    return results


def create_db():
    with closing(pymysql.connect(
            host='localhost',
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=DictCursor
    )) as connection:
        with connection.cursor() as cursor:
            query = """
            CREATE DATABASE IF NOT EXISTS films_imdb
            """
            cursor.execute(query)


def create_table():
    with closing(pymysql.connect(
            host='localhost',
            user=user,
            password=password,
            charset='utf8mb4',
            db='films_imdb',
            cursorclass=DictCursor
    )) as connection:
        with connection.cursor() as cursor:
            query = """
            CREATE TABLE IF NOT EXISTS films_imdb250
            (id int(11) NOT NULL AUTO_INCREMENT,
            title varchar(100) DEFAULT NULL COMMENT "text",
            release_year varchar(100) DEFAULT NULL COMMENT "text",
            rank_films varchar(100) DEFAULT NULL COMMENT "text",
            PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8
            """
            cursor.execute(query)


def insert_into_table(results):
    with closing(pymysql.connect(
            host='localhost',
            user=user,
            password=password,
            charset='utf8mb4',
            db='films_imdb',
            cursorclass=DictCursor
    )) as conn:
        with conn.cursor() as cursor:
            for i in results:
                fs = ','.join(list(map(lambda x: '`' + x + '`', [*i.keys()])))
                vs = ','.join(list(map(lambda x: '%(' + x + ')s', [*i.keys()])))
            query = 'INSERT INTO films_imdb250 %(fs)s VALUES %(vs)s', {'fs': fs, 'vs': vs}
            cursor.executemany(query, results)
            conn.commit()


def main():
    url = f'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    html = get_html(url)
    results = get_all_links(html)
    create_db()
    create_table()
    insert_into_table(results)


if __name__ == '__main__':
    main()
