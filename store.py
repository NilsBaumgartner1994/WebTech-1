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

        # Terms is a dictionary that maps search terms to URIs
        self.terms = {}

        # Pages is a dictionary that maps URIs to data about the page
        self.pages = {}

    def save(self):
        """Save store to pickle file."""
        filename = self.netloc
        filename = re.sub(errorchars, '', filename) # Entferne alle Sonderzeichen
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
        debug = True
        print("Ausgabe: "+ self.pages[page]['html'])
        if debug:
            return self.pages[page]['html']
        return self.pages[page]['html']

    def search(self, q):
        """Search for query string.

        :param q string The full query string.
        """
        dictlist = []
        for url, vorkommen in self.pages.items():
            temp = [url, vorkommen]
            dictlist.append(temp)
        return dictlist
