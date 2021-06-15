import feedparser
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

def nieuwsVanBronnenHalen():
    nu = datetime.datetime.now()
    print("Van start op " + nu.strftime("%H:%M") + ".")
    print("Nieuws ophalen begint over " + str(WAIT_FOR_MINUTES) + " minuten weer.")
    logging.basicConfig(filename='nieuws-ophalen.log', level=logging.INFO)

    logging.info("Het endpoint is '" + BACKEND + "'.")

    # monkey-patch het SSL-certificaat probleem
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    
    custom_header = {"User-Agent": "newsparser"}
    resp = requests.get(GETBRON_VAR, headers=custom_header)

    if resp.status_code != 200:
        logging.critical(f'Status {resp.status_code} teruggekregen.')
    elif resp.status_code == 200:
        logging.info('Lijst met bronnen is opgevraagd.')

    try:
        bronnenLijst = resp.json()
    except ValueError:
        logging.critical("Geen bronnen gevonden!")
        print("Geen bronnen gevonden.")
        bronnenLijst = []

    print(f'Er zijn {len(bronnenLijst)} bronnen gevonden.')

    if(len(bronnenLijst) != 0):
        data=[]
        itemAttributenList=[]
        for b in bronnenLijst:
            bronUrl = b['link_rss']
            print(f'Bron: {bronUrl}')
    
            try:
                bronParse = feedparser.parse(bronUrl)
            except Exception:
                print(f'{bronUrl} kon niet bereikt worden met feedparser, maar we proberen het met een request.')
                try:
                    request = requests.get(bronUrl)
                    if(request.status_code == 200):
                        try:
                            bronParse = feedparser.parse(request.text)
                            print(f'Er is een antwoord met lengte {len(request.text)} voor {bronUrl}.')
                        except Exception as rawparse:
                            print(f'Zelfs met een string werkt de feedparser niet voor {bronUrl}.')
                            logging.critical(f'Zelfs met een string werkt de feedparser niet voor {bronUrl} met fout: {rawparse}')
                    else:
                        print(f'Helaas, antwoord met status {request.status_code} op {bronUrl}.')
                        logging.critital(f'Antwoord met status {request.status_code} op {bronUrl}.')
                except Exception as err:
                    print(f'Zowel feedparser als een request is misgegaan voor {bronUrl}.')
                    logging.critical(f'Misgegaan voor {bronUrl} met: {err}.')
                
            for e in bronParse['entries']:
                # Zoveel mogelijk opschonen van description
                opruimenHtmlTags = re.compile('<.*?>')
                descriptionSchoonVanHtml = re.sub(opruimenHtmlTags, '', e.description)
                descriptionSchoonEscaped = descriptionSchoonVanHtml.replace('"','\\"')
                descriptionSchoonVanWhiteSpace = descriptionSchoonEscaped.replace("&nbsp", "").strip()

                # Publicatiedatum omzetten naar een timestamp
                publicatieDatumZonderTimeZone = ' '.join(e.published.split(' ')[:-1])
                publicatieDatumTemplate = '%a, %d %b %Y %H:%M:%S'
                element = datetime.datetime.strptime(publicatieDatumZonderTimeZone, publicatieDatumTemplate)
                timestampPublicatie = int(datetime.datetime.timestamp(element)) 

                itemAttributenList.append({"title": e.title, "link": e.link, "timestamp_publicatie": timestampPublicatie, "description": descriptionSchoonVanWhiteSpace})

        print(f'Er zijn in totaal {len(itemAttributenList)} items gevonden.')
        foutenGevondenList = []
        #  ombatterijen naar int ipv list
        aantalBestaatAlInt = 0
        aantalToegevoegdInt = 0 
        i = len(itemAttributenList)
        for item in itemAttributenList:
            time.sleep(0.5)
            if 'title' in item:
                i = i-1
                itemJson = json.dumps(item)
                custom_header = {"Content-Type": "application/json"}
                respPost = requests.post(POSTITEM_VAR, data=itemJson, headers=custom_header)
                if respPost.status_code != 200:
                    foutenGevondenList.append(item['title'])
                elif respPost.status_code == 200:
                    try:
                        data = respPost.json()
                        if 'artikel_bestaat_al' in data['resultaat']:
                            aantalBestaatAlInt += 1
                            print(f'{i} x')
                        elif 'goed' in data['resultaat']:
                            aantalToegevoegdInt += 1
                            print(f'{i} v')
                        else:
                            logging.critical(f'Het antwoord op item toevoegen was niet goed.')
                                   
                    except ValueError as err:
                        logging.critical(f'Bij toevoegen item kwam een fout: {err}')
                        print(f'Bij toevoegen item kwam een fout: {err}')

        print(f'Er zijn {aantalBestaatAlInt} items gevonden die al bekend zijn.')
        print(f'Er zijn {aantalToegevoegdInt} nieuwe items gevonden.')

        if len(foutenGevondenList) == 0:
            print(f'Nieuwsverzamelen klaar, met 0 fouten.')
        else:
            logging.warn(f'Nieuwsverzamelen afgerond met {len(foutenGevondenList)} fouten.')
            for fout in foutenGevondenList:
                logging.warning('Fout: ' + fout)

schedule.every(WAIT_FOR_MINUTES).minutes.do(nieuwsVanBronnenHalen)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
