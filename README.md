# ebay-find-completed

eBay removed the very useful `findCompletedItems` endpoint from their api. Now we have to scrape their website. 😒

## Install

```
pip install ebay-find-completed
```

## Quickstart

```python
import asyncio

from ebay_find_completed import search

asyncio.get_event_loop().run_until_complete(search('a rare collectible'))
```
