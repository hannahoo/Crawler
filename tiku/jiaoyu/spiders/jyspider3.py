# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from jiaoyu.items import QuestionAnswer
import logging


class JyspiderSpider(scrapy.Spider):
    name = "jyspider3"
    allowed_domains = ["www.tiku.cn"]
    #domains="http://www.tiku.cn/questions_index/1.html"
    start_urls = (
        'http://www.tiku.cn/questions_index/1.html',
	'http://www.tiku.cn/questions_index/57.html',
	'http://www.tiku.cn/questions_index/3168.html',

    )
    
    
    #parse start page
    def parse(self, response):
        
        
        html=response.xpath('//ul[@class="treeview"]/li/ul/li').extract()
        sec =response.xpath('//ul[@class="treeview"]/li/ul/li/a/text()').extract()

        for i in range(0,len(html)):

            til = Selector(text=html[i]).xpath('//li/ul/li').extract()

            for j in til:
                title = Selector(text=j).xpath('//a/text()').extract_first()
                #url = Selector(text=j).xpath('//a/@href').extract_first()
                title_id = Selector(text=j).xpath('//a/@href').re("\d+")
                # start from page 1 for each title
                yield self.request_page(sec[i],title,title_id[0],1)

    def request_page(self,section,title,title_id,page):

        url="/questions/index/sid/"+str(title_id)
        params="/p/"+str(page)+".html"
        request_url="http://www.tiku.cn"+url+params
        self.logger.debug('start request %s', request_url)
        request=scrapy.Request(url=request_url,callback=self.parse_page,dont_filter=True,meta={'page':page,'section':section,'title':title,'title_id':title_id})
        request.meta['page']=page
        request.meta['section']=section
        request.meta['title']=title
        request.meta['title_id']=title_id
        return request

    def parse_page(self,response):
        page=response.meta['page']
        section=response.meta['section']
        title = response.meta['title']
        title_id=response.meta['title_id']
        self.logger.debug('response from title=%s,page=%d', title,page)
        

        question_list=response.xpath('//div[@class="content"]//fieldset//span[@class="fieldtip"]/a[1]/@href').extract()

        if (len(question_list)==0):
            pass
        else:
            for href in question_list:
                comp_href='http://www.tiku.cn'+href
            
                yield scrapy.Request(url=comp_href,callback=self.parse_question_answer,dont_filter=True,meta={'question_url':comp_href,'title':title,'section':section})
            
            self.logger.debug('end parse_question_list')
            
            total_page=response.xpath('//div[@class="seolist"]/a[last()]').re("\d+")
            if len(total_page)<2:
                total_page=1
            else:
                total_page=int(total_page[1])
        
            if (page==1 and total_page>1):
                for p in range(2,int(total_page)+1):
                    #for p in range(2,3):
                    self.logger.debug('start page for total_page=%s,page=%s', total_page,p)
                
                    yield self.request_page(section,title,title_id,p)
            else:
                pass



    def parse_question_answer(self,response):
        question_html='\n'.join(response.xpath('//fieldset[@class="quesborder"]/div[@class="pt1" or @class="pt2"]//*').extract())


        question_text='\n'.join(response.xpath('//fieldset[@class="quesborder"]/div[@class="pt1" or @class="pt2"]//text()').extract())


        answer_html='\n'.join(response.xpath('//fieldset[@class="quesborder"]/div[@class="pt5" or @class="pt6 per_answer"]//*').extract())
        answer_text='\n'.join(response.xpath('//fieldset[@class="quesborder"]/div[@class="pt5" or @class="pt6 per_answer"]//text()').extract())
        question_url =  response.meta['question_url']
        title = response.meta['title']
        section = response.meta['section']

        item=QuestionAnswer();
        item['question_html']=question_html.replace('\r','').replace('\n','')
        if not question_text:
            item['question_text']=''
        else:
            item['question_text']=question_text.replace('\r','').replace('\n','')
        item['answer_html']=answer_html.replace('\r','').replace('\n','')

        if not answer_text:
            item['answer_text']=''
        else:
            item['answer_text']=answer_text.replace('\r','').replace('\n','')

        if not question_url:
            item['question_url']=''
        else:
            item['question_url']=question_url
        if not title:
            item['title']=''
        else:
            item['title']=title
        if not section:
            item['section']=''
        else:
            item['section']=section



        return item






    
