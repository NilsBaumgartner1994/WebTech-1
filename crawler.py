"""crawler.py

Web crawler using Requests library. Backend is in store.py.

@author: Tobias Thelen
@contact: tobias.thelen@uni-osnabrueck.de
@licence: public domain
@status: completed
@version: 1 (10/2018)

Sie KOENNEN die hier vorgeschlagene Struktur nutzen, müssen das aber nicht.
Alle Vorschläge sollen nur eine Hilfe für diejenigen sein, die lieber mit
etwas mehr Anleitung vorgehen wollen.

"""

import urllib.parse  # parse urls
import posixpath  # path related functions
import re  # regular expressions

import requests  # the requests library for reliable http client code


class Crawler:
    """Fetches pages, extracts links and feeds the search index."""

    def __init__(self, store):
        self.store = store  # the Store object as search index
        self.queue = ['/']  # we start at root
        self.visited = []   # and have not visited anything yet

    def get_links(self, html, path):
        """Extract links to other pages (same domain only) from html and adds to quere. Normalizes links.

        :param html string The cleaned html content of a page.
        :param path string The current page's absolute path.
        :return None
        """
        #print("AusgabeHTML: ", html)
        linkpattern = "((.|[\r\n]+)*?)"
        fullpattern = "href\s*=\s*("+"'"+ linkpattern + "'" + "|" + '"' + linkpattern + '")'
        link_search = re.finditer(fullpattern, html, re.IGNORECASE)
        if link_search:
            for element in link_search:
                link = element.group(0)
                # Reduzieren des Links auf den Link selbst
                link = re.sub('href\s*=\s*', '', link).strip()
                link = re.sub('"*', '', link).strip()
                link = re.sub("'*", '', link).strip()

                if "http:" not in link and "https:" not in link and "www." not in link:

                    #Domain holen
                    #domain_search = re.search('([^/]|(//))*', link, re.IGNORECASE)
                    #if domain_search:
                        #link_domain = domain_search.group(0)
                        #print("Domain: ", link_domain)
                        #print("Rest: ", re.sub(link_domain, '', link).strip())
                        #if True or not link_domain or link_domain == "" or self.store.netloc in link_domain:

                            #print("PfadStart: ", path)

                            #print("PfadEnd: ", path)

                            #if self.store.netloc in link_domain:

                    #wandle alle Links zu absoluten Links
                    path = re.sub('[^/]*$', '', path).strip()
                    link = re.sub('^'+path, '', link).strip()
                    domRelLink = path+link
                    domRelLink = re.sub('//', '/', domRelLink).strip()

                    if domRelLink not in self.visited and domRelLink not in self.queue:
                        print("EndLink: ", domRelLink)
                        self.queue.append(domRelLink)

        return None

    @staticmethod
    def get_title(html):
        """Extract title from raw html.

        :param html string The raw page content.
        :return string The title.
        """
        title_search = re.search('<title>(.*?)</title>', html, re.IGNORECASE)
        title = "Kein Titel gefunden!"
        if title_search:
            title = title_search.group(1)
        return title

    @staticmethod
    def clean(raw_html):
        """Remove unwanted content from html file.
           Steps are:
           1. Remove script, style and head tags and their content
           2. Remove html comments
           3. Remove all HTML tags
           4. Collapse all white space to single spaces

        :param raw_html string The raw page content.
        :return string The cleaned html.
        """

        raw_html = re.sub('(<script)((.|[\r\n]+)*?)(</script>)', '', raw_html, re.IGNORECASE).strip() #entferne Scripts
        raw_html = re.sub('(<style)((.|[\r\n]+)*?)(</style>)', '', raw_html, re.IGNORECASE).strip() #entferne Styles
        raw_html = re.sub('(<head)((.|[\r\n]+)*?)(</head>)', '', raw_html, re.IGNORECASE).strip() #entferne Header
        raw_html = re.sub('(<)((.|[\r\n]+)*?)(>)', '', raw_html).strip() #entferne Tags und Comments
        raw_html = re.sub('\s+', ' ', raw_html).strip() #entferne Whitespace
        return raw_html

    def fetch(self, path):
        """Fetch a url and store page.

        :param path string the (absolute) url to fetch.
        :return None
        """
        domain = self.store.netloc
        self.queue.remove(path)
        req = requests.get(domain+path)
        if req.status_code == 200 and 'html' in req.headers['Content-type']:
            self.visited.append(path)
            self.get_links(req.text, path)
            page = {'title': self.get_title(req.text), 'html': self.clean(req.text)}
            self.store.pages[path] = page
        else:
            print('error 404 page not found')
        return None

    def crawl(self):
        """Fetch pages and follow links. Build search database."""
        count = 0
        while self.queue:
            print("Queue: ", self.queue)
            self.fetch(self.queue[0])
            count += 1
            if count > 20:
                return True
        return True

