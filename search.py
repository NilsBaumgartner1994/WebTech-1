#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webbrowser

from server.webserver import Webserver, App
from store import Store, load_store
from crawler import Crawler
#from myHTML import myHTML

class SearchApp(App):
    """
    Webanwendung für eine Suchmaschine auf einer Domain.

    Diese sehr einfache Anwendung demonstriert die Verwendung des Server-Frameworks.
    Die Klasse SearchApp benötigt zwei Methoden:
    1. Registrierung der Routen
    2. Definition eines Request-Handlers
    """

    def __init__(self, s, **kwargs):
        self.store = s
        App.__init__(self, **kwargs)  # super init

    def register_routes(self):
        self.add_route('', self.search)  # there is only one route for everything

    def pageStart(self):
        return """<style>

* {margin: 0; padding: 0;}

div {
  margin: 20px;
}

ul {
  list-style-type: none;
  width: 500px;
}

h3 {
  font: bold 20px/1.5 Helvetica, Verdana, sans-serif;
}

h4 {
  font: bold 12px/1.5 Helvetica, Verdana, sans-serif;
}

li img {
  float: left;
  margin: 0 15px 0 0;
}

li p {
  font: 200 12px/1.5 Georgia, Times New Roman, serif;
}

li {
  padding: 10px;
  overflow: auto;
}

li:hover {
  background: #eee;
  cursor: pointer;
}

#rcorners2 {
    border-radius: 25px;
    border: 2px solid #73AD21;
    padding: 20px;
    width: 200px;
    height: 150px;
}

</style><br><hr/><br><ul>"""

    def pageEnd(self):
        return """</ul>"""

    def addFound(self, url, count ,title, teaser):
        msg = """<li><h1>({amount}): """.format(amount=count) + title + """</h1>"""
        msg += """<h2><p><a href = "{domain}{link}">{link}</a></p></h2>""".format(
            domain=self.store.netloc, link=url)

        msg += """<p>""" + teaser + """</p>"""

        msg += """</li><hr />"""  # horizonatal Line

        return msg


    def search(self, request, response, pathmatch=None):
        msg = ''
        q = ''
        if 'q' in request.params:  # check if parameter is given
            q = request.params['q']
            hitlist = self.store.search(q)
            msg = "<h2>Ergebnis für <i>'{}'</i></h2>".format(q)

            msg += self.pageStart()
            if hitlist != None:
                #print(hitlist)
                for (url, values) in hitlist:
                    msg += self.addFound(url,values,self.store.pages[url]['title'],self.store.get_teaser(url, q))
            msg += self.pageEnd()

        response.send_template('templates/search/search.tmpl', {'q': q, 'netloc': self.store.netloc, 'msg': msg})


if __name__ == '__main__':
    # entry = 'https://www.inf.uni-osnabrueck.de'
    # entry = 'https://www.virtuos.uni-osnabrueck.de'
    entry = 'http://vm009.rz.uos.de'

    s = load_store(entry)
    if not s:
        s = Store(entry)
        c = Crawler(s)
        c.crawl()
        s.save()

    w = Webserver()
    w.add_app(SearchApp(s, prefix=''))
    w.serve()
    webbrowser.open_new_tab("http://localhost:8080/")