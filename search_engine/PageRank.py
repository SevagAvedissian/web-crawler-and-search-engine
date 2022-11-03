import os
import pickle
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

def build_graph(path):
    print("building graph...")
    rootdir = path

    with open("Data/DocIDdict.txt", "rb") as f:
        docIDdict = pickle.load(f)

    counter = 0
    
    graph = {}
    #initialize graph to empty adjacency list
    for page in docIDdict:
        graph[page] = [0, []]

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            counter += 1
            path = os.path.join(subdir, file)
            with open(path) as f:
                data = json.load(f)
            
            content = data['content']
            url = data["url"]
            soup = BeautifulSoup(content, 'html.parser')

            numLinks = 0
            for link in soup.find_all('a'):
                numLinks += 1
                href = link.get('href')
                if href is None:
                    continue
                elif '#' not in href and not href.startswith("http"):
                    href = urljoin(data["url"], href)

                if url in docIDdict and href in docIDdict and url not in graph[href][1]:
                    if urlparse(href).netloc != urlparse(url).netloc:
                        graph[href][1].append(url)

            if url in docIDdict:
                graph[url][0] = numLinks

    with open("Data/WebGraph.txt", "wb+") as f:
        pickle.dump(graph, f)

def compute_pagerank(graph, iterations=20, dampening=0.15):
    print("computing pagerank...")

    with open(graph, "rb") as f:
        graph = pickle.load(f)

    pageRanks = {}
    n = len(graph)
    
    #initialize all ranks to 1/n
    for page in graph:
        pageRanks[page] = 1/n

    #compute pagerank for i iterations
    for i in range(iterations):
        for page in graph:
            pageRankSum = 0
            for link in graph[page][1]:
                pageRankSum += pageRanks[link] / graph[link][0]
            pageRanks[page] = dampening/n + (1-dampening)*pageRankSum

        #normalize all page ranks
        pageRanksSum = sum(pageRanks[page] for page in pageRanks)
        for page in pageRanks:
            pageRanks[page] /= pageRanksSum

    with open("Data/PageRanks.txt", "wb+") as f:
        pickle.dump(pageRanks, f)
