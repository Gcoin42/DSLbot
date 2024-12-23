import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import math
from config import config

def fetch_lianjia(url=None, num_records=None):
    """
    Fetch property data from Lianjia and return as a list of records.
    """
    if url is None:
        url = config['lianjia']['url']
    if num_records is None:
        num_records = config['lianjia']['num_records']
    headers = config['lianjia']['headers']

    data = []
    page = 1
    while len(data) < num_records and page <= 16:
        try:
            response = requests.get(f"{url}pg{page}/", headers=headers)
            print(f"Fetching data from {url}pg{page}/")
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch data from {url}pg{page}/: {e}")
            return data, False

        soup = BeautifulSoup(response.text, 'html.parser')
        houses = soup.find_all('li', class_='resblock-list')

        for house in houses:
            if len(data) >= num_records:
                break
            name = house.find('a', class_='name').text.strip()
            category = house.find('span', class_='resblock-type').text.strip()
            location_tag = house.find('div', class_='resblock-location')
            if location_tag:
                location_spans = location_tag.find_all('span')
                district = location_spans[0].text.strip() if len(location_spans) > 0 else None
                area = location_spans[1].text.strip() if len(location_spans) > 1 else None
                address = location_tag.find('a').text.strip() if location_tag.find('a') else None
            else:
                district = area = address = None
            house_type_tag = house.find('a', class_='resblock-room')
            if house_type_tag:
                house_types = house_type_tag.text.strip().split('/')
                house_type = house_types[0].strip() if house_types else None
            else:
                house_type = None
            area_range_tag = house.find('div', class_='resblock-area')
            if area_range_tag:
                area_range = re.findall(r'\d+', area_range_tag.text)
                if len(area_range) == 2:
                    area_size = int((float(area_range[0]) + float(area_range[1])) / 2)
                else:
                    area_size = None
            else:
                area_size = None
            price_per_sqm = int(house.find('span', class_='number').text.strip())
            total_price_range_tag = house.find('div', class_='second')
            if total_price_range_tag:
                total_price_range = re.findall(r'\d+', total_price_range_tag.text)
                if len(total_price_range) == 2:
                    total_price = math.ceil((float(total_price_range[0]) + float(total_price_range[1])) / 2)
                elif len(total_price_range) == 1:
                    total_price = int(total_price_range[0])
                else:
                    total_price = None

            data.append([name, category, district, area, address, house_type, area_size, price_per_sqm, total_price])
        page += 1

    return data, True