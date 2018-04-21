import scrapy

class FormSpider(scrapy.Spider):
	name = "form"
	start_urls = []

	def parse(self, response):
		forms = response.css('form') # selects all form elements
		for form in forms:
			# processes each form element
			formItem = FormItem()
            formItem['url'] = response.url
            form_id = form.css('::attr(id)').extract_first()
            if form_id is None:
                form_id = ''
            formItem['form_id'] = form_id
            print (formItem)
            # processes the input elements within each form
            inputs = form.css('input')
            for input in inputs:
                inputItem = InputItem()
                inputItem['form_id'] = form_id
                inputItem['complete'] = input.extract()
                inputItem['type_attr'] = input.css('::attr(type)').extract()
                print(inputItem)

class ParamSpider(scrapy.Spider):
	name = "param"
	start_urls = []

	def parse(self,	response):
		