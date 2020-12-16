import json
import typing
import asyncio

import pyppeteer

from .helpers import alist
from .element import Element


class Scraper:
    query: str = None
    items: typing.Dict = None
    pages: int = 1

    @classmethod
    async def find_completed_items(cls, context, query: str, from_page: int = 1):
        self = Scraper()

        page = await context.newPage()
        await page.goto(f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={query}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={from_page}&_ipg=200')

        page_results = await page.evaluate('''
            () => {
                let results = [];
                let pagesContainer = document.querySelector(".pagination__items");

                document.querySelectorAll(".s-item__wrapper ").forEach((item) => {
                    let title = item.querySelector("h3").outerHTML;
                    let date = item.querySelector(".s-item__title--tagblock").outerHTML;
                    let url = item.querySelector("h3").parentNode.getAttribute("href").outerHTML;
                    let image = item.querySelector("img").getAttribute("src").outerHTML;
                    let price = item.querySelector(".s-item__price").outerHTML;
                    let sold = item.querySelector(".s-item__endedDate").outerHTML;
                    let bids = item.querySelector(".s-item__bidCount");
                    let shipping = item.querySelector(".s-item__logisticsCost");

                    if (bids) { bids = bids.outerHTML; }
                    if (shipping) { shipping = shipping.outerHTML; }

                    results.push({
                        title: title,
                        date: date,
                        url: url,
                        image: image,
                        price: price,
                        sold: sold,
                        bids: bids,
                        shipping: shipping
                    })
                });

                pages = [];

                if (pagesContainer) {
                    pagesContainer.childNodes.forEach((li) => {
                        pages.push(parseInt(li.textContent))
                    });
                } else {
                    pages = [1];
                }

                return {
                    items: results,
                    pages: pages
                };
            }
        ''')

        for item in page_results['items']:
            for k, v in item.items():
                e = Element(v, kill_tags=['span']) if item[k] else None
                
                if e:
                    if k in ['image']:
                        item[k] = e.get('src')
                        continue

                    if k in ['title']:
                        e.clean()

                    item[k] = e.text()

        self.items = {from_page: page_results['items']}
        self.pages = page_results['pages']

        await page.close()

        return self


async def search(query: str, get_all_pages: bool = False) -> typing.List:
    browser = await pyppeteer.launch(headless=True)
    context = await browser.createIncognitoBrowserContext()

    s = await Scraper.find_completed_items(context, query)

    items = s.items
    page_count = s.pages

    print('pg\tpages')

    if get_all_pages:
        if len(page_count) > 1:
            async for pn in alist(page_count):
                asyncio.sleep(1)
                page_items = await Scraper.find_completed_items(context, query, from_page=pn)
                
                page_items_page_count = page_items.pages

                print(f'{pn}\t{page_count}\tgot: {len(page_items.items[pn])} listings')

                items.update(page_items.items)

    return s.items


