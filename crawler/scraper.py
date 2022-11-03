import re
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import hashlib
import shelve
from itertools import combinations
from difflib import SequenceMatcher
from hyperlink import URL

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    #dont crawl if response status is not 200
    try:
        if resp.status_code != 200 or resp.text is None: 
            print("NOT 200")
            return list()
    except AttributeError:
        return list()

    #dont crawl if content is not html
    try:
        if "text/html" not in resp.headers["Content-Type"]:
            return list()
    except KeyError:
        return list()


    links = []

    #dont crawl if raw response if longer than 500k characters
    if len(resp.text) > 500000:
        return list()

    #parse html
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    #get all links from html
    base_url = URL.from_text(url)
    for link in soup.find_all('a', href=True):
        try:
            #join base url and relative url to get absolute url
            full_link = base_url.click(link.get("href"))
            #remove fragmant portion of url
            full_link = full_link.replace(fragment="")
            links.append(full_link.to_text())
        except:
            pass
    return links
	
def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|svg"
            + r"|png|tiff?|mid|mp2|mp3|mp4|mpg"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|bib)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise