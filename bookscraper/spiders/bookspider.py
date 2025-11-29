import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        """Ro'yxat sahifasini parsing qilish"""
        books = response.css("article.product_pod")

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()

            yield response.follow(relative_url, callback=self.parse_book_page)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_page(self, response):

        yield {
            'title': response.css('h1::text').get(),
            'category': response.css('ul.breadcrumb li:nth-child(3) a::text').get(),
            'stars': response.css('p.star-rating::attr(class)').get().split()[-1],
            'description': response.css('#product_description + p::text').get(),
            'upc': response.xpath('//th[text()="UPC"]/following-sibling::td/text()').get(),
            'product_type': response.xpath('//th[text()="Product Type"]/following-sibling::td/text()').get(),
            'price_excl_tax': response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').get(),
            'price_incl_tax': response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').get(),
            'tax': response.xpath('//th[text()="Tax"]/following-sibling::td/text()').get(),
            'availability': response.xpath('//th[text()="Availability"]/following-sibling::td/text()').get().strip(),
            'num_reviews': response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').get(),
        }