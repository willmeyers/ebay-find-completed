import typing
import asyncio

import pyppeteer


class Scraper:
    query: str = None
    url: str = None

    context = None
    page = None

    items: typing.List = None


    @classmethod
    async def find_completed_items(cls, query: str):
        self = Scraper()
        self.context = await pyppeteer.launch(headless=True)

        self.page = await self.context.newPage()
        await self.page.goto(f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={query}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1')

        self.items = await self.page.evaluate('''
            () => {
                return {
                    items: document.getElementsByTagName("div")
                };
            }
        ''')

        await self.context.close()

        return self


async def main():
    s = await Scraper.find_completed_items('thing')
    print(s.items)

asyncio.get_event_loop().run_until_complete(main())
