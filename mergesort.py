def mergesort(results):
    if len(results) <= 1:
        return results
    else:
        linkeListe = results[0:int(len(results)/2)]        
        rechteListe = results[int(len(results)/2):len(results)]
        linkeListe = mergesort(linkeListe)
        rechteListe = mergesort(rechteListe)
        return merge(linkeListe, rechteListe)

def merge(linkeListe, rechteListe):
    neueListe = []
    while (len(linkeListe) > 0 and len(rechteListe) >0):
        if int(linkeListe[0].getYear()) <=  int(rechteListe[0].getYear()):
            neueListe.append(linkeListe[0])
            linkeListe = linkeListe[1:len(linkeListe)]
        else:
            neueListe.append(rechteListe[0])
            rechteListe = rechteListe[1:len(rechteListe)]
            
    while len(linkeListe)>0:
        neueListe.append(linkeListe[0])
        linkeListe = linkeListe[1:len(linkeListe)]
        
    while len(rechteListe)>0:
        neueListe.append(rechteListe[0])
        rechteListe = rechteListe[1:len(rechteListe)]
    return neueListe
