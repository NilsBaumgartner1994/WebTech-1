"""store.py

Search index Backend for web crawler (crawler.py) and search page (search.py).

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 1 (10/2018)

Sie KÖNNEN die hier vorgeschlagene Struktur nutzen, müssen das aber nicht.
Alle Vorschläge sollen nur eine Hilfe für diejenigen sein, die lieber mit
etwas mehr Anleitung vorgehen wollen.

"""

import os.path  # path related functions
import re  # regular expressions
import pickle


errorchars = '[ ?.!/;:]' # Alle Sonderzeichen, welche nicht mit abgespeichert werden sollen

def load_store(netloc):
    """Tries to load the store from pickled file.

    :param netloc string The server to crawl.
    :return store Unpickled store object or None.
    """

    filename = netloc
    filename = re.sub(errorchars, '', filename) # Entferne alle Sonderzeichen

    if not os.path.isfile(filename):
        return None

    infile = open(filename, 'rb')
    loaded = pickle.load(infile)
    infile.close()
    return loaded


class Store:
    """The search index."""

    def __init__(self, netloc):
        """Constructor.

        :param netloc string The server/authority including protocol to crawl (e.g. http://vm009.rz.uos.de)
        """
        self.netloc = netloc

        self.debug = False

        # Terms is a dictionary that maps search terms to URIs
        self.terms = {}

        # Pages is a dictionary that maps URIs to data about the page
        self.pages = {}

    def save(self):
        """Save store to pickle file."""
        filename = self.netloc
        filename = re.sub(errorchars, '', filename) # Entferne alle Sonderzeichen
        if not self.debug:
            outfile = open(filename, 'wb')
            pickle.dump(self, outfile) # Speichere in Datei
            outfile.close()
        return True

    def add(self, url, html, title):
        """Add a page to the store.

        :param url string The pages full url.
        :param html string The cleaned page content (just words).
        :param title string The page's title.
        """
        self.pages[url] = { 'title': title, 'html': html }
        return True

    def get_teaser(self, page, q):
        """Get a short teaser text for a term on a page.

        :param page string The page URL
        :param q string The search string
        :return A short teaser text from page including term.
        """

        html = self.pages[page]['html']
        if self.debug:
            return html
        query = re.sub('\s+', '|', q.strip()).strip() #mehrere querrys gesplittet mit oder
        print("Query:", query)
        word_search = re.findall("(([^\.]*)("+query+")([^\.]*?)[\.:])", html, flags=re.IGNORECASE)  #finde saetze um query ergebnisse
        print("Teaser Sentence:", word_search)
        if word_search: #wenn was gefunden
            all_teaser = ""
            print("Teaser Sentence Count:", len(word_search))
            for i in range(0,len(word_search)): #fuer alle gefundenen
                teaser, finds = re.subn("(?P<query>("+query+"))", r'<mark>\1</mark>', word_search[i][0].strip(), flags=re.IGNORECASE) #markiere alle woerter in den saetzen
                teaser = re.sub('\s+', ' ', teaser).strip()  # entferne Whitespace
                all_teaser = all_teaser + teaser + " ... "
            return all_teaser.strip()[:-4] #entferne letzen drei punkte

        return ""

    def search(self, q):
        """Search for query string.

        :param q string The full query string.
        """

        if q in self.terms: # wenn bereits gefunden, gebe aus
            print("Term found:", self.terms[q])
            return self.terms[q]


        dictlist = [] #anscheinend neu
        for url, vorkommen in self.pages.items():
            query = re.sub('\s+', '|', q).strip() #teile den query auf
            word_search = re.findall(query, vorkommen['html'], re.IGNORECASE) #finde alle woerter auf der seite
            if word_search: #fuer jeden fund
                print("Word Count:", len(word_search))
                count = len(word_search) #zaehle anzahl
                temp = (url, count)
                if count > 0:
                    dictlist.append(temp) #speichere wenn etwas gefunden


        dictlist = sorted(dictlist, key=lambda x: x[1], reverse=True) #sortiere absteigend nach der anzahl
        self.terms[q]=dictlist
        return dictlist
