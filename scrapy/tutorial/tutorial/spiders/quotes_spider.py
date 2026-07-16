from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "oldNavy"

    async def start(self):
        urls = [
            "https://oldnavy.gap.com/browse/product.do?pid=894176002"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        for next_page in response.css('a::attr(href)').getall():
            yield response.follow(next_page, callback=self.parse)