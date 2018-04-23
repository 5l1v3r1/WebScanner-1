import scrapy
from .. import settings
from ..items import *

class MainSpider(scrapy.Spider):
    name = "main"
    start_urls = [url for url in settings.TARGETS.split('\n') if url]
    allowed_domains = [url.replace('http://', '').replace('https://', '')
            for url in start_urls]

    def parse(self, response):
        self.logger.debug("(parse) response: status=%d, URL=%s" % (
                response.status, response.url))
        # Crawl links
        for href in response.xpath('//a/@href'):
            self.logger.debug("(parse) a href to %s" % href.extract())
            yield response.follow(href, callback=self.parse, meta={
                    'dont_redirect': True,
                    'handle_httpstatus_list': range(300, 309) })

        if -1 < response.url.rfind('?') > response.url.rfind('/'):
            # Output GET
            split = response.url.split('?')
            params = [param.split('=')[0] for param in split[-1].split('&')]
            self.logger.info("(parse) yield GET form at %s" % response.url)
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
            self.logger.info("(parse) yield %s form to %s" % (method, action))
            yield FormItem(action=action.url, method=method, inputs=inputs)
            # Crawl submitted form
            self.logger.debug("(parse) crawl %s form to %s" % (method, action))
            request = scrapy.http.FormRequest.from_response(response, formnumber=i)
            request.meta['dont_redirect'] = True
            yield request
            request = scrapy.http.FormRequest.from_response(response, formnumber=i,
                    formdata={ inp['name']: '1' for inp in inputs })
            request.meta['dont_redirect'] = True
            yield request

        # Follow redirections after crawl
        if 299 < response.status < 399 and 'Location' in response.headers:
            self.logger.debug("(parse) redirecting to %s" % response.headers['Location'])
            yield response.follow(response.headers['Location'], callback=self.parse)