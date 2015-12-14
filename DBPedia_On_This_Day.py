from SPARQLWrapper import SPARQLWrapper, SPARQLWrapper2, JSON
from mergesort import mergesort
from time import localtime
from enum import Enum
import createInfo
import re
import codecs
import copy

#an entry is everything that is needed for an entry on the calender page:
#the year, the information, an additional thumbnail and the pagerank for pages that do not use the indegree for ranking
#the pagerank-attribute is only needed as long as it has to be extracted from a seperate file and not from DBpedia itself
#we can also save the final format that the entry will have (highlighted or not)

class entry():

    def __init__(self, year, info, thumbnail):
        self.year = year
        self.info = info
        self.thumbnail = thumbnail
        self.format = "caption"
        self.pagerank = 0

    def setInfo(self, info):
        self.info = info
        
    def getInfo(self):
        return self.info

    def getYear(self):
        return self.year

    def getThumbnail(self):
        return self.thumbnail

    def setFormat(self, f):
        self.format = f
        
    def getFormat(self):
        return self.format

    def setPagerank(self, p):
        self.pagerank = p
        
    def getPagerank(self):
        return self.pagerank


#set parameters for this execution
sparql = SPARQLWrapper2("http://dbpedia.org/sparql")
numberOfResults = 15

pagerankQueries = ["movie", "writtenWork", "musicalWork"]

personTypes = ["artists", "athletes", "politicians", "scientists", "other", "untyped"]
eventQueries = ["admitted", "signed", "battles", "battles2", "beatified", "buildingEnd", "buildingStart", "canonized", "coronations", "dateRatified", "destructions", "discoveries", "dissolutions", "executed", "firstAirDate", "firstAscent", "firstFlight", "flag", "foundations", "musical", "opened", "play", "royalAssent", "shipLaunched"]
workQueries = ["movie", "musicalWork", "writtenWork", "game"]

anniversaries = [entry(0, "", "")]
validAnniversaries = [1000, 500, 250, 200, 150, 100, 75, 50, 25, 10]

time = localtime()
year = time[0]




def Day(day):
    if(str(day).endswith("1") and str(day) != "11"):
        return str(day)+"st"
    elif(str(day).endswith("2") and str(day) != "12"):
        return str(day)+"nd"
    elif (str(day).endswith("3") and str(day) != "13"):
        return str(day)+"rd"
    else:
        return str(day)+"th"

#the threshold determines which indegree is considered important enough to be highlighted
#this value is a rough estimate and may need to be adapted with new DBpedia versions
def calcThreshold(typ):
    if typ in ["battles", "battles2", "canonized", "coronations", "dateRatified", "destructions", "firstFlight"]:
        return 100
    elif typ in ["buildingEnd", "buildingStart", "opened", "musical", "play", "shipLaunched"]:
        return 50
    elif typ in ["discoveries", "firstAscent"]:
        return 60
    elif typ in ["dissolutions", "foundations"]:
        return 150
    elif typ in ["firstAirDate"]:
        return 500
    else:
        return 20000
    
#query a Result in JSON-Format
#these results are already ranked by InDegree
def queryResults(query, typ):
    results = querying(query)
    print ("Querying, ", typ, "...")
    if typ in pagerankQueries:
        return rankByPagerank(results, typ)
    else:
        return rankByIndegree(results, typ)     

def querying(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)    
    results = sparql.query()
    return results

#this prepares the result set if it is ranked by inDegree
def rankByIndegree(results, typ):
    entries = []
    count = 0
    
    for res in results.bindings:
        count += 1
        #create the information-string depending on the type
        info = getattr(createInfo, typ)(res)
        
        #battles are grouped by the bigger conflict and thus do not return a year
        #therefore they need to be added seperately
        if typ == "battles":
            entries.append(entry(int(res["date"].value[0:4]), info, ""))

        else:
            try:
                entries.append(entry(int(res["date"].value[0:4]), info, res["thumbnail"].value))
            except KeyError:
                entries.append(entry(int(res["date"].value[0:4]), info, ""))


        #afterwards we check if the entry qualifies for highlighting
        threshold = calcThreshold(typ)
        if(int(res["indegree"].value) > threshold) or ("person" in typ and count < 4):
            entries[count-1].setFormat("highlightedCaption")

        #lastly we check for anniversaries
        if (typ in eventQueries) or ("person" in typ and count < 4):
            if ((year - entries[count-1].getYear()) in validAnniversaries):
                anniversaries.append(copy.copy(entries[count-1]))
                
                #if the birth or death of a person has its anniversary, we need to
                #extend the information depending on whether it's a birth or death date
                if(typ == "personBorn"):
                    updatedInfo = str(entries[count-1].getInfo()) + ", was born."
                    anniversaries[-1].setInfo(updatedInfo)
                elif(typ == "personDied"):
                    updatedInfo = str(entries[count-1].getInfo()) + ", died."
                    anniversaries[-1].setInfo(updatedInfo)

        #we only use as many results as specified        
        if(count >= numberOfResults):
            break
        
    return entries


#this prepares the result set if it should be ranked by pagerank
def rankByPagerank(results, typ):
    entries = []
    count = 0
    for res in results.bindings:
        inserted = False
        index = 0
        count += 1 
        info = getattr(createInfo, typ)(res)

        #we search for the pagerank in the pagerank graph
        query = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo:<http://dbpedia.org/ontology/>
        PREFIX vrank:<http://purl.org/voc/vrank#>
        SELECT ?label
        FROM <http://dbpedia.org>
        FROM <http://people.aifb.kit.edu/ath/#DBpedia_PageRank>
        WHERE{	
        ?s vrank:hasRank/vrank:rankValue ?label	
        FILTER (?s = <http://dbpedia.org/resource/America_by_Heart>) .
        }
        """
        #query = createQueryFromFile("Queries/pagerank/pagerank.txt", date)
        query = query.replace("?search", ("<" + res["uri"].value + ">"))
        pageranks = querying(query)
        for key in pageranks.bindings:
            while (not inserted):
                    #...and insert all the results ordered by their pagerank
                try:
                    if(index >= len(entries) or entries[index].getPagerank() < key["label"].value):
                        try:
                            e = entry(int(res["date"].value[0:4]), info, res["thumbnail"].value)
                        except KeyError:
                            e = entry(int(res["date"].value[0:4]), info, "")
                        e.setPagerank(key["label"].value)
                        entries.insert(index, e)
                        inserted = True

                    else:
                        index += 1
                except KeyError:
                    print("meh")
                    break

    for e in entries[0:3]:
        try:
            if ((year - e.getYear()) in validAnniversaries):
                anniversaries.append(copy.copy(e))
            e.setFormat("highlightedCaption")
        except:
            break

    return entries[0:numberOfResults]

    
#create the section in the HTML-page with either a thumbnail or block of text
def createSection(result):
    section = ""
    for res in result:
        section += "<div class=\"wrap\">"
        section += "<div class=\"%s\">%s: %s</div>" % (res.getFormat(), str(res.getYear()), res.getInfo())
        
        if res.getThumbnail() != "":
            section += "<div class=\"thumbnail\"> <img src=\"%s\" /></div>" % (res.getThumbnail())

        section += "</div>"
    return section

#create the section for anniversaries
def createAnni(jub):
    global anniversaries
    anniversaries = mergesort(anniversaries)

    anni = ""
    for i in range (1, len(anniversaries)):
        if (anniversaries[i].getYear() != anniversaries[i-1].getYear()):
            anni += "</ul><br>"
            anni += "%s (%s years ago):<ul>" % (str(anniversaries[i].getYear()), str(year-anniversaries[i].getYear()))
            
        anni += "<li>%s</li>" % (anniversaries[i].getInfo())
    anni = anni[9:len(anni)]
    return anni

#write file in UTF-8 coding
def writeFile(output, filename):
    filename = "Result Pages/DBpedia on the " + filename + ".html"
    with codecs.open(filename, 'w', 'utf-8') as targetFile:
        targetFile.write(output)

#read a query from a file and replace the placeholder with the current date
def createQueryFromFile(src, date):
    file = open(src, "r")

    query = ""

    for line in file:
            query += line.rstrip()
    file.close()
    query = query.replace("datum", date)
    return query

#create the HTML-page for a date
def main(date):

    year, month, day = date

    #create the Date in the format "-Month-Day" to query from DBpedia
    if(len(str(month)) == 1):
        date = "\"-0" + str(month)
    else:
        date = "\"-" + str(month)
    if(len(str(day)) == 1):
        date += "-0" + str(day) + "\""
    else:
        date += "-" + str(day) + "\""

    #"Month" and "Day" transfer the date to natural text
    months = ["January", "Februar", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    DATE = Day(day) + " of " + months[month - 1]
    
    print ("Creating a calender page for the ", date)

    
    #query the information and save it into arrays
    
    #1. birth- and death dates
    births = []
    deaths = []
    for p in personTypes:
        births.append(queryResults(createQueryFromFile("Queries/birthDate/" + p + ".txt", date), "personBorn"))
        deaths.append(queryResults(createQueryFromFile("Queries/deathDate/" + p + ".txt", date), "personDied"))

    #the birth and death dates for "other" and "untyped" are merged together
    births[4].extend(births[5])
    deaths[4].extend(deaths[5])

    #2. general events
    generalEvents = []
    for e in eventQueries:
        generalEvents.extend(queryResults(createQueryFromFile("Queries/events/" + e + ".txt", date), e))

    #3. published work
    works = []
    for w in workQueries:
        works.extend(queryResults(createQueryFromFile("Queries/work/" + w + ".txt", date), w))

    #create an entry sentence 
    ENTRY = "The " + DATE + " is the " + Day(time[7]) +" of the year."

    #open the HTML-template and replace each of the placeholder-strings with the sorted result-list
    html = ""
    file = open("template.txt", "r")
    for line in file:
            html += line.rstrip()
    file.close()
    html = html.replace("ENTRY", ENTRY)
    html = html.replace("DATE", DATE)
    html = html.replace("ANNIVERSARIES", createAnni(mergesort(anniversaries)))
    html = html.replace("ARTISTSB", createSection(mergesort(births[0])))
    html = html.replace("ARTISTSD", createSection(mergesort(deaths[0])))
    html = html.replace("ATHLETESB", createSection(mergesort(births[1])))
    html = html.replace("ATHLETESD", createSection(mergesort(deaths[1])))
    html = html.replace("POLITICIANSB", createSection(mergesort(births[2])))
    html = html.replace("POLITICIANSD", createSection(mergesort(deaths[2])))
    html = html.replace("SCIENTISTSB", createSection(mergesort(births[3])))
    html = html.replace("SCIENTISTSD", createSection(mergesort(deaths[3])))
    html = html.replace("OTHERB", createSection(mergesort(births[4])))
    html = html.replace("OTHERD", createSection(mergesort(deaths[4])))
    html = html.replace("EVENTS",createSection(mergesort(generalEvents)))
    html = html.replace("PUBLICATIONS", createSection(mergesort(works)))
    
    writeFile(html, "DBpediaOT_" + date + "_" + month")

if __name__ == "__main__":
    main()
            

            
