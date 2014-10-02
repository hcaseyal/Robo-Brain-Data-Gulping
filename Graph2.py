import rdflib
#We need requests for a weird error about OpenCyc formatting, they do not specify that they are using xml
import requests

#Get some naming edge names
from rdflib.namespace import RDF
from rdflib.namespace import RDFS
from rdflib.namespace import OWL
from sets import Set

#Re-define edges for readibility
InstanceOfEdge = RDF.type
TypeOfEdge = RDFS.subClassOf
OutsideSourceURL = OWL.sameAs
NameOfId = rdflib.term.URIRef(u'http://sw.cyc.com/CycAnnotations_v1#label')
PrettyString  = rdflib.term.URIRef(u'http://sw.opencyc.org/concept/Mx4rwLSVCpwpEbGdrcN5Y29ycA')
wikiURL = rdflib.term.URIRef(u'http://sw.opencyc.org/concept/Mx4rNv0nbm4TTjOp7yhmnzOyqg')

#Set
Visited = Set([])

def printRelation(subject, str, object, graph, outFile):
    "Prints the given relation between subject and object"
    str1= "{}{}{}{}".format(getTextName(subject, graph), str, getTextName(object, graph), "\n")
    outFile.write(str1)

def getTextName(subject, graph):
    "Gets the text name for the subject URI, if it exists"
    if (subject,NameOfId,None) in graph:
        for s,p,o in graph.triples( (subject, NameOfId, None) ):
            return o

def printSourceURLs(thing, graph, outFile):
    "Prints the outside source URLS for the thing, if they exist"
    if(thing, OutsideSourceURL, None) in graph:
        for s,p,o in graph.triples( (thing, OutsideSourceURL, None) ):
            str1= "{}{}{}{}".format(s, ' has outside source URL of ',o,"\n")
            outFile.write(str1)

def printWikiURL(thing, graph, outFile):
    "Prints the wiki URL for the thing, if it exists"
    if(thing, wikiURL, None) in graph:
        for s,p,o in graph.triples( (thing, wikiURL, None) ):
            str1= "{}{}{}{}".format(s, ' has wiki ',o, "\n")
            outFile.write(str1)

def printURI(thing, graph, outFile):
    "Prints the URI for the thing"
    outFile.write("{}{}{}{}".format(getTextName(thing, graph), ' has URI ', thing, "\n"))

def printGraph(graph, outFile, Neighbors):
    "Prints all relevant information for the given graph and stores relevant nodes in a set"
    #RDF uses (subj,pred,obj), look for all data about shoe
    for subject,predicate,obj in graph:
    
        #InstanceOf edges, excluding those with w3 links
        if predicate==InstanceOfEdge and obj.find("w3.org") == -1:
            printRelation(subject,' is instance of ',obj, graph, outFile)
            Neighbors.add(subject)
            Neighbors.add(obj)
        
        #TypeOf edges
        elif predicate==TypeOfEdge:
            printRelation(subject,' is type of ',obj, graph, outFile)
            Neighbors.add(subject)
            Neighbors.add(obj)
    
        #Aliases
        elif predicate==PrettyString:
            outFile.write("{}{}{}{}".format(getTextName(subject, graph), ' is alias of ', obj, "\n")) #obj (the alias) is already in text form

        else:
            continue

        printURI(subject, graph, outFile)
        printWikiURL(subject, graph, outFile)

def crawlGraph(URI, outFile, numLayers, count=0):
    "Crawls the graph for the given number of layers from the starting URI i.e, 0 means just request the starting node graph, 1 means all its immediate neighbors, etc"
    #Start with Shoe, and request the web page (sent GET request)
    resp = requests.get(URI)
    #Adds to set of visited nodes
    Visited.add(URI)
    #Set of neighbors to potentially visit
    Neighbors = Set([])
    #Parse the returned result via rdflib
    g = rdflib.Graph()
    g.parse(data=resp.content,format="xml")
    printGraph(g, outFile, Neighbors)

    if (count >= numLayers):
        return

    #Get set of relevant nodes to visit that haven't been visited yet.
    for node in (Neighbors-Visited):
        crawlGraph(node, outFile, numLayers, count+1)

#Edit here
f=open('Starting Nodes.txt', 'r')
for line in f:
    arr = line.split() #First string in file is URI, second is name of output file
    resp = requests.get(arr[0])
    g = rdflib.Graph()
    g.parse(data=resp.content,format="xml")
    outFileName = arr[1]
    outFile=open(outFileName, 'w') #file to populate
    
    Visited.clear()
    crawlGraph(arr[0], outFile, 1)
    outFile.close()
f.close()
