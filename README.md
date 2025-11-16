# ebay-find-completed

eBay removed the very useful `findCompletedItems` endpoint from their api. Now we have to scrape their website. 😒

## Install

```
pip install ebay-find-completed
```

## Usage

### Basic Search

```python
import asyncio
from ebay_find_completed import search

# Search for completed listings
results = asyncio.run(search('vintage camera'))
print(results)
```

### Get All Pages of Results

By default, only the first page is returned. To scrape all available pages:

```python
import asyncio
from ebay_find_completed import search

# Get all pages of results (may take longer)
results = asyncio.run(search('pokemon cards', get_all_pages=True))
```

### Understanding the Results

The search returns a dictionary where keys are page numbers and values are lists of items:

```python
{
    1: [
        {
            'title': 'Vintage Canon AE-1 35mm Camera',
            'price': '$125.00',
            'sold': 'Sold Nov 10, 2025',
            'url': 'https://www.ebay.com/itm/...',
            'image': 'https://i.ebayimg.com/...',
            'date': 'Nov 10',
            'bids': '15 bids',
            'shipping': '+$12.50 shipping'
        },
        # ... more items
    ],
    2: [ ... ]  # if get_all_pages=True
}
```

### Working with Results

```python
import asyncio
from ebay_find_completed import search

async def find_average_price(query):
    results = await search(query, get_all_pages=True)

    prices = []
    for page_num, items in results.items():
        for item in items:
            # Extract numeric price (remove $ and convert to float)
            price_str = item['price'].replace('$', '').replace(',', '')
            try:
                prices.append(float(price_str))
            except ValueError:
                continue

    if prices:
        avg_price = sum(prices) / len(prices)
        print(f"Average price for '{query}': ${avg_price:.2f}")
        print(f"Found {len(prices)} sold items")
        return avg_price

    return None

# Run it
asyncio.run(find_average_price('nintendo switch'))
```

### Available Fields

Each item in the results contains:

- `title` - Item title
- `price` - Final sale price
- `sold` - Date the item sold
- `url` - Link to the eBay listing
- `image` - URL to item image
- `date` - Short date format
- `bids` - Number of bids (if auction)
- `shipping` - Shipping cost (if available)
