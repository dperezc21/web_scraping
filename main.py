from common import config
import news_pages_object as news
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
import re
from datetime import datetime
import csv

link_formed = re.compile(r'^https?://.+/.+$')
link_root = re.compile(r'^/.+$')


def _run(periodico):

    host = config()["periodicos"][periodico]["url"]

    homepage = news.HomePage(periodico, host)
    articles = []
    for link in homepage.article_links:
        article = _fetch_article(periodico, host, link)
        if article:
            articles.append(article)
    _save_articles(periodico, articles)


def _fetch_article(periodico, host, link):
    print("fetching in",link)
    article = None
    
    try:
        article = news.ArticlePage(periodico, _build_link(host,link))
    except (HTTPError, MaxRetryError) as e:
        print("hubo un error al consultar la web")

    if article and not article.body:
        
        print("articulo invalido")
        return None

    return article

        
def _build_link(host, link):
    if link_formed.match(link):
        return link
    elif link_root.match(link):
        return '{}{}'.format(host, link)
    else:
        return '{}/{}'.format(host, link)
    

def _save_articles(periodico,articles):
    date_doc = datetime.now().strftime('%Y-%m-%d')
    
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
    out_file_name = '{}_{}_articles.csv'.format(periodico, date_doc)
    with open(out_file_name, "w+", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)
            

if __name__ == '__main__':
    lista_periodicos = config()["periodicos"]
    for p in lista_periodicos:
        print(p)
    periodico = input("ingrse un periodico: ")
    _run(periodico)