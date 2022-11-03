ABOUT
---

This is an implementation of a web crawler that downloads and scrapes webpages which are then indexed by a search engine. Web crawler supports multithreading while still behaving politely and abiding by each website's robots exclusion protocol. Search engine uses tf-idf scoring to retrieve relevant webpages and PageRank to order them based on importance.

INSTALLATION
---

Download source and install dependencies

```
git clone https://github.com/SevagAvedissian/web-crawler-and-search-engine
pip install -r requirements.txt
```

EXECUTION
---

### Crawler

Execute launch_crawler.py to begin crawling.
```python launch_crawler.py```

Crawler manages a local store of urls waiting to be crawled. Exectuion of crawler can be stopped and started back up at any point. To restart crawler, delete the Data/frontier.* files and run launch_crawler.py

### Search Engine

Execute launch_search.py to create index and compute PageRank.
```python launch_search.py```

Subequent execution os launch_search.py will use the index and other bookeeping datastructures stored locally. To restart the search engine delete the files found in Data/search_engine/ and execute launch_search.py

CONFIGURATION
---

The following configuration fields are available in config.ini

**[CRAWLER]**<br>
*SEEDURL* : List of urls that crawler will start from<br>
*POLITENESS* : Delay between two requests made to the same server<br>
*THREADCOUNT* : Number of concurrent threads crawling

