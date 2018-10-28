#!/usr/bin/env python
# -*- coding: utf-8 -*-

class myHTML:
    """An app wraps web applications or reusable components for
       web applications such as serving static files, providing
       statistical information on the server.

       An app registers it routes with the server and provides
       callbacks for these routes.
       """
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

</style><br><hr/><br><br><ul>"""

    def pageEnd(self):
        return """</ul>"""

    def addFound(self, url, title, teaser):
        msg = """<li><h1>"""+title+"""</h1>"""
        msg += """<h2><p><a href = "{link}">{link}</a></p></h2>""".format(
                        link=url)

        msg+= """<p>"""+teaser+"""</p>"""

        msg += """</li><hr />""" # horizonatal Line

        return msg