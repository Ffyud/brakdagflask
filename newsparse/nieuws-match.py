from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import schedule
import requests
import logging
import json
import time
import sys

BACKEND = sys.argv[1]
GET_ITEMS = BACKEND + "/items"
POST_VERGELIJKING = BACKEND + "/item/vergelijkbaar"
WAIT_FOR_MINUTES = 30

def nieuwsVergelijken():
    custom_header = {"User-Agent": "newsparser"}
    resp = requests.get(GET_ITEMS, headers=custom_header)

    logging.info('Items ophalen en vergelijken.')

    if resp.status_code != 200:
        logging.critical(resp.status_code)
    elif resp.status_code == 200:
        itemsVergelekenList = []

        try:
            itemLijst = resp.json()
            vergelijkLijst = resp.json()
            logging.info("Items gevonden om te vergelijken.")
        except ValueError:
            logging.critical("Geen items gevonden!")
            print("Oeps, geen items gevonden.")
            itemLijst = []
            vergelijkLijst = []
            
        for item in itemLijst:
            item1 = item['title']
            id1 = item['id']
            for itemVergelijk in vergelijkLijst:
                item2 = itemVergelijk['title']
                id2 = itemVergelijk['id']
                vergelijkPercentage = fuzz.ratio(item1, item2)
                if(vergelijkPercentage > 53 and vergelijkPercentage < 100):
                    itemsVergelekenList.append({"item": id1, "item_compare": id2, "match_percentage": vergelijkPercentage})

        for item in itemsVergelekenList:
            if 'item' in item:
                itemJson = json.dumps(item)
                custom_header = {"Content-Type": "application/json"}
                respPost = requests.post(POST_VERGELIJKING, data=itemJson, headers=custom_header)
                if respPost.status_code != 200:
                    logging.critical(resp.status_code)
                elif respPost.status_code == 200:
                    try:
                        data = respPost.json()
                        if 'vergelijking_ingediend' in data['resultaat']:
                            logging.info("Vergelijking ingediend!")
                        else:
                            logging.critical("Geen goed antwoord op vergelijking!")
                    except ValueError:
                        logging.critical("Bij toevoegen vergelijking kwam geen response!")
                        print("Oeps, bij toevoegen vergelijking kwam geen response.")            

schedule.every(WAIT_FOR_MINUTES).minutes.do(nieuwsVergelijken)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
