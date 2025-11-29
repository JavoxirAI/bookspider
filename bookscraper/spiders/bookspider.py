import scrapy
from bookscraper.items import BookscraperItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        """Ro'yxat sahifasini parsing qilish"""
        books = response.css("article.product_pod")

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            book_url = response.urljoin(relative_url)
            yield scrapy.Request(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_page(self, response):
        item = BookscraperItem()

        item['url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['category'] = response.css('ul.breadcrumb li:nth-child(3) a::text').get()
        item['stars'] = response.css('p.star-rating::attr(class)').get().split()[-1]
        item['description'] = response.css('#product_description + p::text').get()
        item['upc'] = response.xpath('//th[text()="UPC"]/following-sibling::td/text()').get()
        item['product_type'] = response.xpath('//th[text()="Product Type"]/following-sibling::td/text()').get()
        item['price_excl_tax'] = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').get()
        item['price_incl_tax'] = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').get()
        item['tax'] = response.xpath('//th[text()="Tax"]/following-sibling::td/text()').get()
        item['availability'] = response.xpath('//th[text()="Availability"]/following-sibling::td/text()').get().strip()
        item['num_reviews'] = response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').get()

        yield item