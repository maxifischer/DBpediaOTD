import re
##prepare the string but keep URIs intact
##this is necessary if the information contains links to other DBpedia pages
def prepareString(string):
    string = string.replace("*", "")
    lastKomma = string.rfind(",")
    if(lastKomma > 0):
        string = string[0:lastKomma] + " and " + string[lastKomma +1:len(string)]
    #if the string is empty (because GROUP_CONCAT returned "") raise a KeyError
    if(len(string) > 0):
        return string
    else:
        raise KeyError
    string = re.sub(" +", " ", string)
    string = string.replace("and and", "and")
    string = string.replace(".,", ",")
    return string


## prepare the String and also remove URIs
def prepareStringWithURI(string):
    if("," in string):
        strings = string.split(",")
        string = ""
        for s in strings:
            string += s[s.rfind("/")+1:len(s)] + ", "
        string = string[0:len(string)-2]
    else:
        string = string[string.rfind("/")+1:len(string)]
    string = prepareString(string)
    string = string.replace("-", " ")
    string = string.replace("_", " ")
    return string

def link(res):
    return "<a href=\"%s \">%s</a>" % (res["uri"]["value"], res["name"]["value"])

def aN(string):
    if string[0] in ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]:
        return "an %s" % string
    return "a %s" % string


##Sentence for persons
def Person(res):
    return "%s, %s" % (link(res),(aN(prepareStringWithURI(res["info"]["value"]))))

def personBorn(res):
    return Person(res)

def personDied(res):
    return Person(res)

##Sentence for grouped queries
def grouped(res, apposition, verb):
    entities = prepareString(res["info"]["value"])
    if(res["info"]["value"].count("</a>") >= 2):
        return "The %ss %s were %s." %(apposition, entities, verb)
    else:
        return "The %s %s was %s." %(apposition, entities, verb)

def signed(res):
    return grouped(res, "act", "signed")

def dateRatified(res):
    return grouped(res, "body of rules and regulations", "ratified")

def flag(res):
    return grouped(res, "flag", "adopted")

def royalAssent(res):
    return grouped(res, "act", "assented")        

def shipLaunched(res):
    return grouped(res, "ship", "launched")

def firstFlight(res):
    return grouped(res, "plane", "launched")


##Sentece for foundations and dissolutions
        
def foundedOrDissolved(res, verb):
    typ = aN(prepareStringWithURI(res["kind"]["value"]))
    try:
        f = prepareStringWithURI(res["founder"]["value"])
        founder = " Its founder was %s." % (f)
    except:
        founder = ""
    try:
        p = prepareStringWithURI(res["products"]["value"])
        products = " It is associated with %s." % (p)
    except KeyError:
        products = ""
        
    if "Organisation" in typ:
        return "The %s, %s, was %s.%s%s" % (link(res), typ, verb, founder, products)
    return "%s, %s, was %s.%s%s" % (link(res), typ, verb, founder, products)
        
def dissolutions(res):
    return foundedOrDissolved(res, "dissolved")

def foundations(res):
    return foundedOrDissolved(res, "founded")

##Beatifications, Coronations, Crowned

def entitlements(res, verb):
    try:
        description = aN(prepareStringWithURI(res["info"]["value"]))
        by = prepareStringWithURI(res["by"]["value"])
        return "%s, %s, was %s by %s." % (link(res), description, verb, by)
    
    except KeyError:
        description = aN(prepareStringWithURI(res["info"]["value"]))
        return "%s, %s, was %s." % (link(res), description, verb)

def beatified(res):
    return entitlements(res, "beatified")

def canonized(res):
    return entitlements(res, "canonized")

def coronations(res):
    return entitlements(res, "crowned")

##Buildings

def building(res, action, verb):
    try:
        typ = prepareStringWithURI(res["buildingType"]["value"])
        return "The %s %s %s %s." % (action, typ, link(res), verb) 
    except KeyError:
        return "The %s %s %s." % (action, link(res), verb) 


def buildingStart(res):
    return building(res, "construction of the", "started")

def buildingEnd(res):
    return building(res, "construction of the", "was finished")

def destructions(res):
    return building(res, "", "was destroyed")


##Other senteces, that cannot be summarized

def admitted(res):
    try:
        country = prepareStringWithURI(res["country"]["value"])
        return "%s was admitted to %s." % (link(res), country)
    except KeyError:
        return "%s was admitted." % (link(res))
    
def battles(res):
    biggerConflict = "<a href=\"%s\">%s</a>" % (res["biggerConflict"]["value"], res["biggerConflictName"]["value"])
    battles = prepareString(res["info"]["value"])
    temp = battles.rpartition("SEP")
    if(temp[1]=="SEP"):
        battles = temp[0]+ " and " + temp[2]
        battles = battles.replace("SEP", ", ")
    battles = battles.replace(";", ", ")
    battles = battles.replace(".,", ",")
    return "During the %s %s, took place." % (biggerConflict, battles)

def battles2(res):
    try:
        results = prepareStringWithURI(res["results"]["value"])
        return "The %s, which resulted in %s, took place." %(link(res), results)
    except KeyError:
        return "The %s took place." %(link(res))
    
def discoveries(res):
    try:
        discoverer = prepareStringWithURI(res["discoverer"]["value"])
        return "%s, a celestial body, was discovered by %s." % (link(res), discoverer)
    except KeyError:
        return "%s, a celestial body, was discovered." % (link(res))
    
def executed(res):
    try:
        order = prepareStringWithURI(res["objective"]["value"])
        return "The operation %s with the order \" %s \" was executed." % (link(res), order)
    except KeyError:
        return "The Operation %s was executed." % (link(res))

def firstAirDate(res):
    info = prepareString(res["info"]["value"])
    return "%s aired for the first time." % (info)

def firstAscent(res):
    try:
        ascentor = prepareStringWithURI(res["by"]["value"])
        output =  "%s was first ascented by %s." % (link(res), ascentor)
    except KeyError:
        output = "%s was first ascented by." % (link(res))
        
    try:
        h = prepareStringWithURI(res["height"]["value"])
        height = " It is %s m high." % (h)
    except KeyError:
        height = ""
    return "%s %s" % (output, height)
       
def musical(res): 
    try:
        composer = prepareStringWithURI(res["musicBy"]["value"])
        return "The musical %s premiered. Its music was written by %s." %(link(res), composer)
    
    except KeyError:
        return "The musical %s premiered." %(link(res))

def opened(res):
    return "%s opened." %(link(res))

def play(res):
    try:
        genre = prepareStringWithURI(res["genre"]["value"]) 
    except KeyError:
        genre = ""
        
    try:
        writer = prepareStringWithURI(res["writer"]["value"])
        output = "The %s play %s by %s premiered." % (genre, link(res), writer)
    except KeyError:
        output = "The %s play %s premiered." % (genre, link(res))
        
    try:
        s = prepareStringWithURI(res["subject"]["value"])
        subject = "It's subject is %s." %(s)
    except KeyError:
        subject = ""
    return "%s %s" % (output, subject)

def writtenWork(res):
    try:
        author = prepareStringWithURI(res["author"]["value"])
        output = "The piece of written work %s written by %s was published." % (link(res), author)
    except KeyError:
        output = "The piece of written work %s was published." % (link(res))
    try:
        g =  prepareStringWithURI(res["genres"]["value"])
        genres = "It belongs to the %s genre." %(g)
    except KeyError:
        genres = ""
    return "%s %s" % (output, genres)

def musicalWork(res):
    try:
        a = prepareStringWithURI(res["artists"]["value"]) 
        artists = ", which was interpreted by %s," %(a)
    except KeyError:
        artists = ""
    try:
        g = prepareStringWithURI(res["genres"]["value"])
        genres = " It belongs to the %s genre." % (g)
    except KeyError:
        genres = ""
    if "Single" in res["isKindOf"]["value"]:
        return "The song %s %s was released.%s" % (link(res), artists, genres)
    else:
        return "The album %s %s was released.%s" % (link(res), artists, genres)
        
def movie(res):
    try:
        if(res["gross"]["value"][len(res["gross"]["value"])-2] == "E"):
            gross = float(res["gross"]["value"][0:len(res["gross"]["value"])-2])
            gross = gross*(10**int(res["gross"]["value"][len(res["gross"]["value"])-1]))
            gross = str(int(gross)) + " $"
        else:
            gross = res["gross"]["value"] + "$"
        gross = ", which grossed " + gross + ", "
    except KeyError:
        gross = ""
    
    try:
        a = prepareStringWithURI(res["actors"]["value"])
        actors = "It, among others, featured %s." % (a)
    except KeyError:
        actors = ""
    return "The movie %s %s was released. %s" % (link(res), gross, actors)
        
def game(res):
    return "The first release of the game series %s was published." %  (link(res))
