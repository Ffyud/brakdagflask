import feedparser
import html
import ssl
import json
import requests
import re
import datetime
import schedule
import time
import logging
import sys

BACKEND = sys.argv[1]
GETBRON_VAR = BACKEND + "/bron"
POSTITEM_VAR = BACKEND + "/item"
WAIT_FOR_MINUTES = 7

def nieuws_van_bronnen_halen():
    nu = datetime.datetime.now()
    logging.basicConfig(filename='nieuws-ophalen.log', level=logging.INFO)

    # monkey-patch het SSL-certificaat probleem
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    
    custom_header = {"User-Agent": "newsparser"}
    try:
        resp = requests.get(GETBRON_VAR, headers=custom_header)

        if resp.status_code != 200:
            logging.critical(f'Status {resp.status_code} teruggekregen.')
    except Exception as err:
        logging.critical(f'Bevragen van bronnen mislukt, service lijkt stuk!')

    try:
        bronnen_lijst = resp.json()
    except Exception:
        logging.critical("Geen bronnen gevonden!")
        bronnen_lijst = []

    if(len(bronnen_lijst) != 0):
        data=[]
        item_attributen=[]
        for b in bronnen_lijst:
            bron_url = b['link_rss']
    
            try:
                bron_parse = feedparser.parse(bron_url)
            except Exception:
                logging.critical(f'{bron_url} kon niet bereikt worden met feedparser, maar we proberen het met een request.')
                try:
                    request = requests.get(bron_url)
                    if(request.status_code == 200):
                        try:
                            bron_parse = feedparser.parse(request.text)
                        except Exception as rawparse:
                            logging.critical(f'Zelfs met een string werkt de feedparser niet voor {bron_url} met fout: {rawparse}')
                    else:
                        logging.critital(f'Antwoord met status {request.status_code} op {bron_url}.')
                except Exception as err:
                    logging.critical(f'Misgegaan voor {bron_url} met: {err}.')
                
            for e in bron_parse['entries']:
                # Zoveel mogelijk opschonen van description
                opruimen_html = re.compile('<.*?>')
                descr_zonder_html = re.sub(opruimen_html, '', e.description)
                descr_zonder_escape = descr_zonder_html.replace('"','\\"')
                descr_zonder_whitespace = descr_zonder_escape.replace("&nbsp", "").strip()

                # Publicatiedatum omzetten naar een timestamp
                pubdate_zonder_timezone = ' '.join(e.published.split(' ')[:-1])
                pubdate_format = '%a, %d %b %Y %H:%M:%S'
                item_datetime = datetime.datetime.strptime(pubdate_zonder_timezone, pubdate_format)
                item_timestamp_pubdate = int(datetime.datetime.timestamp(item_datetime)) 

                title = html.unescape(e.title)
                descr_unescaped = html.unescape(descr_zonder_whitespace)

                item_attributen.append({"title": title, "link": e.link, "timestamp_publicatie": item_timestamp_pubdate, "description": descr_unescaped})

        fouten_gevonden = []
        #  ombatterijen naar int ipv list
        aantal_al_bestaand = 0
        aantal_toegevoegd = 0 
        i = len(item_attributen)
        for item in item_attributen:
            time.sleep(0.5)
            if 'title' in item:
                i = i-1
                itemJson = json.dumps(item)
                custom_header = {"Content-Type": "application/json"}
                try:
                    post_response = requests.post(POSTITEM_VAR, data=itemJson, headers=custom_header)
                    if post_response.status_code != 200:
                        fouten_gevonden.append(item['title'])
                    elif post_response.status_code == 200:
                        try:
                            data = post_response.json()
                            if 'artikel_bestaat_al' in data['resultaat']:
                                aantal_al_bestaand += 1
                            elif 'goed' in data['resultaat']:
                                aantal_toegevoegd += 1
                            else:
                                logging.critical(f'Het antwoord op item toevoegen was niet goed.')
                        except ValueError as err:
                            logging.critical(f'Bij toevoegen item kwam een fout: {err}')
                except Exception as err:
                    logging.critical(f'Mis gegaan met posten van artikel: {err}')

        if len(fouten_gevonden) != 0:
            logging.warn(f'Nieuwsverzamelen afgerond met {len(fouten_gevonden)} fouten.')
            for fout in fouten_gevonden:
                logging.warning('Fout: ' + fout)

schedule.every(WAIT_FOR_MINUTES).minutes.do(nieuws_van_bronnen_halen)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
