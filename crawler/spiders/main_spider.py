import scrapy
from .. import settings
from ..items import *

class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = [url for url in settings.TARGETS.split('\n') if url]
    allowed_domains = [url.replace('http://', '').replace('https://', '')
            for url in start_urls]

    def parse(self, response):
        # Crawl links
        for a in response.css('a'):
            yield response.follow(a, callback=self.parse)

        if -1 < response.url.rfind('?') > response.url.rfind('/'):
            # Output GET
            split = response.url.split('?')
            params = [param.split('=')[0] for param in split[-1].split('&')]
            yield FormItem(action=''.join(split[:-1]), method='GET',
                    inputs=[InputItem(name=p) for p in params if p])
        else: params = []

        # Crawl forms
        for i,form in enumerate(response.css('form')):
            # Output
            action = response.follow(form.xpath('@action').extract_first(''))
            method = form.xpath('@method').extract_first('GET')
            inputs = [InputItem(name=inp.xpath('@name').extract_first())
                    for inp in form.css('input,select,textarea,button')
                    if inp.xpath('@name')
                    and inp.xpath('@name').extract_first('') not in params]
            if not inputs: continue
            yield FormItem(action=action.url, method=method, inputs=inputs)
            # Crawl
            yield scrapy.http.FormRequest.from_response(response, formnumber=i)
            yield scrapy.http.FormRequest.from_response(response, formnumber=i,
                    formdata={ inp['name']: '1' for inp in inputs })
