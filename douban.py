import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import config

def fetch_douban():
    """
    Fetch top 250 movies from Douban and return as a DataFrame.
    """
    headers = config['douban']['headers']
    url = config['douban']['url']
    movies = []
    for start_num in range(0, 250, 25):
        response = requests.get(f"{url}?start={start_num}", headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        all_titles = soup.findAll('span', attrs={'class': 'title'})
        all_rating_num = soup.findAll('span', attrs={'class': 'rating_num'})
        all_evaluate_num = soup.findAll('div', attrs={'class': 'star'})
        all_inq = soup.findAll('span', attrs={'class': 'inq'})

        cn_all_titles = []
        for title in all_titles:
            title_string = title.get_text()
            if '/' not in title_string:
                cn_all_titles.append(title_string)

        for title, rating_num, evaluate_num, inq in zip(cn_all_titles, all_rating_num, all_evaluate_num, all_inq + [None] * (len(cn_all_titles) - len(all_inq))):
            rating_num_string = rating_num.get_text()
            evaluate_num_string = evaluate_num.find_all('span')[-1].get_text()
            inq_string = inq.get_text() if inq else ""
            movies.append([title, rating_num_string, evaluate_num_string, inq_string])

    df = pd.DataFrame(movies, columns=['Title', 'Rating', 'Evaluate Number', 'Inq'])
    return df