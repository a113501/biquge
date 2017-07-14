import scrapy
from scrapy import Request
from biquge.items import BiqugeItem, ChapterContentItem

class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    base_url = 'http://www.qu.la'

    def start_requests(self):
        for i in range(5):
            start_url = 'http://zhannei.baidu.com/cse/search?q=&p={0}&s=920895234054625192&srt=def&nsid=0&entry=1'.format(i)
            yield Request(start_url, callback=self.get_novel_url)

    def get_novel_url(self, response):
        novel_urls = response.xpath('//*[@id="results"]/div[3]/div/div[2]/h3/a/@href').extract()
        for i in novel_urls:
            yield Request(i, callback=self.parse_novel_link)


    def parse_novel_link(self, response):
        base_url = 'http://www.qu.la'
        book = BiqugeItem()
        book['novel_link'] = response.url
        book['novel_id'] = response.url.replace('http://www.qu.la/book/','').replace('/','')
        book['novel_name'] = response.xpath('//*[@id="info"]/h1/text()').extract()
        book['author'] = response.xpath('//*[@id="info"]/p[1]/text()').extract()[0].replace('作\xa0\xa0者：','')
        book['introduce'] = response.xpath('//*[@id="intro"]/text()').extract()[0].replace(' ','').replace('\r','').replace('\n','')

        chapter_link = response.xpath('//*[@id="list"]/dl/dd/a/@href').extract()
        for i in chapter_link:
            yield Request(base_url+i, callback=self.parse_chapter_link, meta={'book_info':book})

    def parse_chapter_link(self, response):
        book = {}
        book_info = response.meta
        chapter=ChapterContentItem()
        chapter['chapter_name'] = response.xpath('//*[@id="wrapper"]/div[6]/div[2]/div[2]/h1/text()').extract()
        chapter['chapter_content'] = ''
        chapter['chapter_id'] = response.url.replace(book_info['book_info']['novel_link'],'').replace('.html','')
        for i in response.xpath('//*[@id="content"]/text()').extract():
            chapter['chapter_content'] = chapter['chapter_content'] + i.replace('\u3000','').replace('\xa0','').replace('\r','').replace('\n','').replace('\t','')

        book['info'] = book_info['book_info']
        book['all_chapter'] = chapter

        return book
