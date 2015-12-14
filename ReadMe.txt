DBpediaOTD ist ein Programm, mit dem ähnlich der Wikipedia "On this day"-Seite fuer jeden Tag eine HTML-Seite mit den wichtigsten Ereignissen, Geburts- und Todesdaten an diesem Tag.

Das Projekt ist als docker-Container angelegt. Um das Projekt zu laden, muss folgender Befehl ausgeführt werden:
docker build -t dbpediaotd --file ./Dockerfile .

Um die Kommandozeile für die Ausführung zu öffnen, wird folgender Befehl ausgeführt:
docker run -it dbpediaotd bash

Jetzt kann das Programm wie ein gewöhnliches Python-Programm auf der Kommandozeile ausgeführt werden mit verschiedenen Kommandozeilenoptionen. Der grundsätzliche Aufruf ist:
python DBpediaOTD.py

Mit der Option "-open" kann eine HTML-Seite angezeigt werden. Hinter "-open" muss der Name der Datei genannt werden. Die Seiten sind nach dem Schema "DBpediaOT_<Monat>_<Tag>" abgespeichert, also bspw. "DBpediaOT_12_1" (dem 1. Dezember).

Außerdem gibt es die Option "-reload", bei der die HTML-Seite eines Tages neu berechnet wird. Die Eingabe erfolgt dabei nach dem Schema "-reload <Jahr> <Monat> <Tag>", also z.B. "-reload 2015 12 1" (für den 1. Dezember). Wenn anstatt des Datums "all <Jahr>" angegeben wird, werden alle Dateien des angegebenen Jahres neu berechnet.
