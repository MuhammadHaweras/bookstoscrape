import scrapy
import random

from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    
    user_agents_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    ]
    
    

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            base_url = "https://books.toscrape.com/"
            next_page_url = base_url + ("catalogue/" if "catalogue/" not in relative_url else "") + relative_url
            
            # headers = {"User-Agent": random.choice(self.user_agents_list)}
            
            yield response.follow(next_page_url, self.parse_book_page)
            
            # for paid proxies, #dont need to do anything in settings.py
            # yield response.follow(next_page_url, self.parse_book_page, meta={"proxy": "paidproxylink"})
            

        next_page = response.css("li.next a").attrib["href"]

        if next_page:
            base_url = "https://books.toscrape.com/"
            next_page_url = base_url + ("catalogue/" if "catalogue/" not in next_page else "") + next_page
            yield response.follow(next_page_url, callback=self.parse)
            
    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()
        
        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['product_type'] = table_rows[1].css("td ::text").get()
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get()
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get()
        book_item['tax'] = table_rows[4].css("td ::text").get()
        book_item['availability'] = table_rows[5].css("td ::text").get()
        book_item['num_reviews'] = table_rows[6].css("td ::text").get()
        book_item['stars'] = response.css("p.star-rating").attrib['class']
        book_item['category'] = response.xpath('//ul[@class="breadcrumb"]/li[a[contains(@href, "category")]][last()]/a/text()').get()
        book_item['description'] = response.xpath('//div[@id="product_description"]/following-sibling::p[1]/text()').get()
        book_item['price'] = response.css('p.price_color ::text').get()

        yield book_item