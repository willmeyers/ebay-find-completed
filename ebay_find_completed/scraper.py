import json
import typing
import asyncio

import pyppeteer

from .element import Element


class Scraper:
    query: str = None

    items: typing.List = None

    @classmethod
    async def find_completed_items(cls, context, query: str):
        self = Scraper()

        page = await context.newPage()
        await page.goto(f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={query}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1')

        self.items = await page.evaluate('''
            () => {
                let results = [];

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

                return {
                    items: results
                };
            }
        ''')

        for item in self.items['items']:
            for k, v in item.items():
                print(k, v)
                e = Element(v, kill_tags=['span']) if item[k] else None
                
                if e:
                    if k in ['image']:
                        item[k] = e.get('src')
                        continue

                    if k in ['title']:
                        e.clean()

                    item[k] = e.text()

        await page.close()

        return self


async def fetch(query: str, get_all_pages: bool = False) -> typing.List:
    browser = await pyppeteer.launch(headless=True)
    context = await browser.createIncognitoBrowserContext()

    s = await Scraper.find_completed_items(context, query)

    return s.items

