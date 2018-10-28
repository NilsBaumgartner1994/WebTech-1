## Entwickler:
- Johann Arndt (960402),
- Nils Baumgartner (955625),
- Alexander Tessmer (954425)

# Web-Technologien 18/19: Aufgabe 1 - Suchmaschine

Implementieren Sie in Python eine Suchmaschine, die aus folgenden drei Teilen besteht:

1. Suchindex

    Der Suchindex ist eine Datenstruktur, die Suchbegriffe auf URIs abbildet. Der Suchindex wird vom Web-Crawler befüllt und liefer dann für das Such-Frontend zu jedem Suchanfrage (= Liste von Suchbegriffen) eine sortierte Liste von URIs mit weiteren Informationen (Titel, Vorschauabschnitt). Für diese Aufgabe muss der Suchindex nicht aktualisiert werden können und wird in sehr simpler Form gespeichert.
     
2. Web-Crawler

    Der Web-Crawler ist ein Web-Client, der von einer Startadresse ausgehend Seiten abruft, ihren Inhalt an den Suchindex weitergibt, Links identifiziert und diesen Links folgt. Für diese Aufgabe ruft der Crawler nur die Seiten ab, die zu einer bestimmten, angegebenen Domain gehören.
     
3. Such-Frontend

    Das Such-Frontend ist eine Web-Anwendung, die die Eingabe eines Suchbegriffs erlaubt und mithilfe des Suchindexes eine Trefferliste ausgibt.

## Voraussetzungen
- Python 3.5, 3.6 oder 3.7
- Requests-Library (Installation per `pip install requests`, ggf. in Virtual Environment (s. https://docs.python.org/3/tutorial/venv.html )

## Anforderungen im Detail:

- Suchindex
    - Der Suchindex sollte als ein Objekt der Klasse Store realisiert werden, die in der Datei story.py realisiert wird.
    - Das Store-Objekt sollte eine Instanzvariable netloc (bzw. authority) beinhalten. Das ist die Domain, für die der Suchindex aufgebaut gilt.
    - Das Store-Objekt sollte zwei Dictionaries enthalten. Das Dictionary terms verwendet Begriffe als Schlüssel und enthält URIs sowie die Vorkommenshäufigkeit des Begriffs unter dieser URI als Werte. Das Dictionary pages verwendet URIs als Schlüssel und enthält den gefilterten Text sowie den Titel und ggf. weitere Daten als Werte.
    - Das Store-Objekt sollte eine Methode add haben, über die abgerufene Inhalte vom Web-Crawler hinzugefügt werden können. Die Methode füllt die Dictionaries terms und pages.
    - Das Store-Objekt sollte eine Methode search haben, die für einen übergebenen Suchstring eine sortierte Liste von URIs, Titeln und Vorschautexten (Teaser) liefert. Die Sortierung soll berücksichtigen, ob alle Suchbegriffe enthalten sind und wie häufig ein Suchbegriff auf der Seite vorkommt.
    - Der Suchindex soll mithilfe des pickle-Mechanismus gespeichert und geladen werden können. Damit wird das gesamte Store-Objekt in eine Datei gespeichert bzw. aus ihr geladen. Dies ist keine Datenbank, sondern nur eine Möglichkeit, Speicherinhalte zwischenzuspeichern. Das ist hier sinnvoll, damit die Ergebnisse des Crawlers gesichert werden können. Der Dateiname leitet sich sinnvollerweise aus der netloc-Variablen ab.
- Web-Crawler
    - Der Webcrawler sollte als ein Objekt der Klasse Crawler realisiert werden, die in der Datei crawler.py implementiert wird.
    - Der Webcrawler enthält ein Store-Objekt, sowie eine Liste noch zu besuchender URIs (queue) und eine Liste bereits abgerufener URIs (visited) als Instanzvariable.
    - Mit der Methode crawl soll der Crawl-Vorgang angestoßen werden. Dabei beginnt der Crawler mit der angegebenen Domäne (store.netloc) und dem Pfad / und führt eine Breiten- oder Tiefensuche aus:
        - Seite abrufen (fetch), aus der queue löschen und in visited eintragen
        - Links auf der Seite erkennen und in queue einreihen, wenn zur gleichen Domän gehörig und noch nicht abgerufen (get_links)
        - Titel extrahieren (get_title) und HTML-Code der Seite bereinigen (clean)
        - URI mit Titel und bereinigtem Code an Suchindex übergeben (store.add)
    - Die Methode fetch soll mithilfe der Requests-Bibliothek den http(s)-Request absenden. Nur Respsonses mit Status-Code 200, und einem HTML-Content-Typ sollen weiter verarbeitet werden.
    - Die Methode get_links muss HTML-Links (... oder ...) erkennen, die URIs extrahieren und normieren. Für die Erkennung sind Reguläre Ausdrücke (Python-Module re) zu verwenden. Dazu kann zunächst die Python-Funktion urllib.parse verwendet werden. Normieren bedeutet, dass relative URIs in absolute umgewandelt werden müssen. Für Pfadmanipulationen ist dabei ggf. das Modul posixpath hilfreich. Eventuelle URI-Parameter müssen erhalten bleiben.
    - Die Methode get_title extrahiert mittels eines regulären Ausdrucks den Titel aus einem HTML-Dokument.
    - Die Methode clean bereinigt den HTML-Code z.B. mit folgenden Schritten:
        - Die Tags script, style und head samt Inhalt entfernen.
        - HTML-Kommentare entfernen.
        - Alle HTML-Tags entfernen (nur die Tags, nicht den Inhalt dazwischen!)
        - Aufeinanderfolgende Whitespaces in je ein Leerzeichen umwandeln.
- Such-Frontend
    - Das Such-Frontend wird als App für das in Kapitel 3 vorgestellte Framework in der Datei search.py implementiert.
    - Die Domäne für den Suchindex kann z.B. in einer Konstanten abgelegt werden. Zum Testen verwenden Sie http://vm009.rz.uos.de.
    - Beim Starten soll versucht werden, den Suchindex zu laden. Falls er nicht existiert, soll der Web-Crawler angestoßen werden, um einen Suchindex aufzubauen.
    - Wenn der Suchindex erstellt bzw. geladen ist, soll die Such-App registriert und der Web-Server gestartet werden.
    - Als Vorlage für die Such-App kann die Celsius-App verwendet werden.
    - Die Eingabe des Suchstrings geschieht wie dort über ein einfaches Eingabefeld, dessen Wert als GET-Parameter ausgelesen wird.
    - Statt der Berechnung des Fahrenheit-Wertes wird dann der Suchindex mit der Methode Store.search durchsucht und das Ergebnis als HTML-Code (keine Anforderungen an das Aussehen!) aufbereitet werden.

## Testdaten
Zum Testen können Sie die Domäne http://vm009.rz.uos.de verwenden, die einen sehr kleinen Baum von vier HTML-Seiten enthält.

## Empfohlenes Vorgehen

Es wird folgende Reihenfolge bei der Implementation empfohlen:

1. Implementieren und testen Sie die Methode Crawler.fetch zum Abrufen von einzelnen Seiten
2. Dann sollten die Methoden get_title und get_links folgen, die das Resultat von fetch verarbeiten. Hier sind ggf. die regulären Ausdrück eine Schwierigkeit, fragen Sie dann einfach nach!
3. Wenn get_links funktioniert, können Sie den Crawl-Algorithmus implementieren, der den Links folgt.
4. Anschließend ist clean an der Reihe, um reinen Text aus dem HTML zu machen.
5. Wenden Sie sich erst dann der Klasse Store zu und beginnen Sie dort mit dem Konstruktor und der Methode add. Fügen sie Code hinzu, um die generierten Strukturen ausgeben zu lassen.
6. Anschließend folgt die search-Methode.
7. Laden und Speichern des Stores können am Schluss implementiert werden.
8. Abschließend setzten Sie die Search-App analog zur Celsius-App um.
