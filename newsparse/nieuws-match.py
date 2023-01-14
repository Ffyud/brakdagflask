from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import schedule
import ssl
import datetime
import requests
import logging
import json
import time
import sys

BACKEND = sys.argv[1]
AANTAL_ITEMS = 250
GET_ITEMS = f'{BACKEND}/items/aantal/{AANTAL_ITEMS}'
POST_VERGELIJKING = f'{BACKEND}/item/vergelijkbaar'
WAIT_FOR_MINUTES = 45

def nieuws_vergelijken():
    logging.basicConfig(filename='nieuws-match.log', level=logging.INFO)

    nu = datetime.datetime.now()

    # monkey-patch het SSL-certificaat probleem
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    custom_header = {"User-Agent": "newsparser"}
    
    try:
        resp = requests.get(GET_ITEMS, headers=custom_header)

        if resp.status_code != 200:
            logging.critical(f'Status {resp.status_code} teruggekregen voor bevragen items.')
    except Exception:    
        logging.critical(f'Bevragen van bronnen mislukt, service lijkt stuk!')

    vergeleken_items = []

    try:
        item_lijst = resp.json()
        vergelijk_lijst = resp.json()
    except Exception:
        logging.critical("Vergelijking mislukt, want geen items gevonden!")
        item_lijst = []
        vergelijk_lijst = []
            
    for item in item_lijst:
        time.sleep(1)
        item1 = item['title']
        id1 = item['id']
        for item_vergelijk in vergelijk_lijst:
            item2 = item_vergelijk['title']
            id2 = item_vergelijk['id']
            match_percentage = fuzz.token_sort_ratio(item1.lower(), item2.lower())
            if(match_percentage > 55 and match_percentage < 100):
                vergeleken_items.append({"item": id1, "item_compare": id2, "match_percentage": match_percentage})

    for item in vergeleken_items:
        time.sleep(1)
        if 'item' in item:
            item_json = json.dumps(item)
            custom_header = {"Content-Type": "application/json"}
            try:
                post_response = requests.post(POST_VERGELIJKING, data=item_json, headers=custom_header)
                if post_response.status_code != 200:
                    logging.critical(f'Status {resp.status_code} teruggekregen voor toevoegen vergeleken item.')
            except:
                logging.critical(f'Toevoegen vergelijking mislukt, service lijkt stuk!')

            try:
                data = post_response.json()
            except ValueError:
                logging.critical("Bij toevoegen vergelijking kwam geen response!")

schedule.every(WAIT_FOR_MINUTES).minutes.do(nieuws_vergelijken)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
