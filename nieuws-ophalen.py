import feedparser
import ssl
import json
import requests
import re
import datetime
import logging
import sys

def nieuwsVanBronnenHalen():
    logging.basicConfig(filename='nieuws-ophalen.log', level=logging.WARN)
    # monkey-patch het SSL-certificaat probleem
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    resp = requests.get('http://127.0.0.1:5000/bronnen')
    if resp.status_code != 200:
        logging.critical(resp.status_code)
        sys.exit()
    elif resp.status_code == 200:
        logging.info('Even geduld tot alle stappen zijn doorlopen.')
        logging.info('1/6 Lijst met bronnen is opgevraagd.')
    bronnenLijst = resp.json()
    logging.info('2/6 Er zijn " + str(len(bronnenLijst))+ " bronnen gevonden.')

    data=[]
    dataAlleBronnen=[]
    itemAttributenList=[]
    for b in bronnenLijst:
        bronUrl = b['link_rss']
        bronParse = feedparser.parse(bronUrl)
        
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

    logging.info('3/6 Er zijn in totaal ' + str(len(itemAttributenList)) + ' items gevonden.')
    foutenGevondenList = []
    #  ombatterijen naar int ipv list
    aantalBestaatAlInt = 0
    aantalToegevoegdInt = 0 
    for item in itemAttributenList:
        if 'title' in item:
            itemJson = json.dumps(item)
            custom_header = {"Content-Type": "application/json"}
            respPost = requests.post('http://127.0.0.1:5000/item', data=itemJson, headers=custom_header)
            if respPost.status_code != 200:
                foutenGevondenList.append(item['title'])
            elif respPost.status_code == 200:
                data = respPost.json()
                if 'artikel_bestaat_al' in data['resultaat']:
                    aantalBestaatAlInt += 1
                elif 'goed' in data['resultaat']:    
                    aantalToegevoegdInt += 1

    logging.info('\n4/6 Er zijn ' + str(aantalBestaatAlInt) + ' items gevonden die al bekend zijn.')
    logging.info('5/6 Er zijn ' + str(aantalToegevoegdInt) + ' nieuwe items gevonden.')
    if len(foutenGevondenList) == 0:
        logging.info('\n6/6 Nieuwsverzamelen klaar, met 0 fouten.')
    else:
        logging.info('Nieuwsverzamelen afgerond met ' + str(len(foutenGevondenList)) + ' fouten.')
        for fout in foutenGevondenList:
            logging.warning('Fout: ' + fout)


if __name__ == "__main__":
    nieuwsVanBronnenHalen()