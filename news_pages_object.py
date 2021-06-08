from common import config
from requests import get
from bs4 import BeautifulSoup

class NewsPage:
    def __init__(self,periodico, url):
        self._config = config()["periodicos"][periodico]
        self._queries = self._config["queries"]
        self._html = None
        self._visit(url)


    def _select(self, query_string):
        return self._html.select(query_string)


    def _visit(self,url):
        response = get(url)
        response.raise_for_status()
        self._html = BeautifulSoup(response.text, "html.parser")


class HomePage(NewsPage):

    def __init__(self, periodico, url):
        
        super().__init__(periodico, url)

    
    @property
    def article_links(self):
        list_links = []
        for link in self._select(self._queries["article_link"]):
            if link and link.has_attr("href"):
                list_links.append(link)

        return set(link["href"] for link in list_links)

    
class ArticlePage(NewsPage):

    def __init__(self, periodico, url):
        self._url = url
        super().__init__(periodico, url)

    @property
    def body(self):
        result = self._select(self._queries["article_body"])
        return result[0].text if len(result) else ""

    @property
    def title(self):
        result = self._select(self._queries["article_title"])
        return result[0].text if len(result) else ""
    
    @property
    def url(self):
        return self._url

 