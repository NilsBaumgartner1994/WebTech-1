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
from pathlib import Path


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
        # ToDo: Erster Satz der Seite und erstes vorkommen des Begriffs als Satz zwischen zwei Punkten mit ... getrennt
        # Achtung problem bei mehreren Suchbegriffen

        html = self.pages[page]['html']
        if self.debug:
            return html

        word_search = re.findall("[^\.]*?"+q+"[^\.]*?[.|:].", html, re.IGNORECASE)
        if word_search:
            teaser, finds = re.subn("(?P<query>("+q+"))", r'<mark>\1</mark>', word_search[0].strip(), flags=re.IGNORECASE)
            return teaser.strip()

        return ""

    def search(self, q):
        """Search for query string.

        :param q string The full query string.
        """

        full = q
        parts = q.split()
        #self.terms[full] = [{'count': 1, 'url': ""}]

        #word_search = re.findall(q, html, re.IGNORECASE)
        #if word_search:
            #print("Word Count: ", len(word_search))

        #word_search = re.findall("[^\.]*?"+q+"[^\.]*?[.|:].", html, re.IGNORECASE)
        #if word_search:
            #print("Sentence Count: ", len(word_search))
         #   teaser, finds = re.subn("(?P<query>("+q+"))", r'<mark>\1</mark>', word_search[0].strip(), flags=re.IGNORECASE)
            #print("Replaces: ", finds)
            #print("Sentence: ", teaser)
          #  return teaser.strip()

        #return ""


        #word_search = re.finditer(q, html, re.IGNORECASE)
        #if word_search:
        #    for element in word_search:

        dictlist = []
        for url, vorkommen in self.pages.items():
            temp = [url, vorkommen]
            dictlist.append(temp)
        return dictlist
