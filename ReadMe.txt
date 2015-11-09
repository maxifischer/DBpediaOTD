Die Textdatei für die Pagerank-Dateien ist zu groß, um sie per Mail zu versenden. Daher muss diese runtergeladen werden unter:
http://dbpedia.semanticmultimedia.org/dbpedia2014/en/pagerank_scores_en_2014.ttl.bz2 

Die Datei muss entpackt und als .txt (anstatt .ttl) im Ordner "Knowledge Mining Abgabe Gruppe 4 - DBpedia on this day\Codeabgabe\DBpedia On This Day" gespeichert werden.
______

Damit das Skript ausgeführt werden kann, muss das Modul SPARQLWrapper installiert sein (https://pypi.python.org/pypi/SPARQLWrapper )

1. Runterladen des eggs https://pypi.python.org/packages/2.7/S/SPARQLWrapper/SPARQLWrapper-1.6.4-py2.7.egg#md5=1ff0d9c168ed302f03901d753a1a76c5 
2. Kopieren in den Skript-Ornder der Python-Installation (bei Standard Installation ist der Pfad C:\Python<Versionsnummer>\Scripts). 
3. Commandline in diesen Ordner navigieren.
4."easy_install <SPARQLWrapper-Dateiname>" ausführen. Das Modul wird nun installiert.

Ausführen:

1. Doppelklick auf "DBpedia On This Day.py"
2. Das Programm braucht nun ca. 5 Minuten um die Kalenderseite für den heutigen Tag zu erstellen - das Ergebnis ist ein html-Dokument mit entsprechender Datumsbezeichnung im Ordner "Result Pages". 

Sollte keine Datei entstehen, ist entweder der SPARQLWrapper nicht installiert oder DBpedia wird grade gewartet. In diesem Fall das Skript über Rechtsklick -> EDIT with IDLE öffnen und mit F5 ausführen. Dann wird eine Fehlermeldung angezeigt. 

______

Enthaltene Dateien:

"Queries" - Alle Abfragen, nach Abschnitt sortiert
"Result Pages" - enthält die Ergebnisseiten (hier ist auch ein Stylesheet und zwei Logos. Diese müssen vorhanden sein, damit die Seite richtig angezeigt wird)
"pagerank_scores_en_2014.txt" - Pagerank-Werte 
"template.txt" - HTML Vorlage 
"createInfo.py" - Modul zur Erstellung der natürlichsprachlichen Sätze
"mergesort.py" - Mergesort-Implementation zur Sortierung der Einträge anhand ihres Jahres



