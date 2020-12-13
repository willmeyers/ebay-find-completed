import typing
import asyncio

import pyppeteer


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

                document.querySelectorAll(".s-item__info ").forEach((item) => {
                    let title = item.querySelector("h3").textContent;

                    results.push({
                        title: title
                    })
                });

                return {
                    items: results
                };
            }
        ''')

        await page.close()

        return self


async def main():
    browser = await pyppeteer.launch(headless=True)

    context = await browser.createIncognitoBrowserContext()

    s = await Scraper.find_completed_items(context, 'thing')
        
    print(s.items)

asyncio.get_event_loop().run_until_complete(main())
