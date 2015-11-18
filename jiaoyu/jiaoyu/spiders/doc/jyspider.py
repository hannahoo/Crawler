# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from jiaoyu.items import QuestionAnswer
#import logging


class JyspiderSpider(scrapy.Spider):
    name = "jyspider"
    allowed_domains = ["mofangge.com"]
    start_urls = (
        'http://www.mofangge.com/qlist/wuli/',

    )

    def parse(self, response):
        subjects=['huaxue','shengwu','zhengzhi','lishi','dili']
        pages['huaxue']=
        pages['shengwu']=
        pages['zhengzhi']=
        pages['lishi']=
        pages['dili']=

        for x in subjects:
            yield self.request_page(i,1)

    def request_page(self,subjects,page):
        request_url='http://www.mofangge.com/qlist/'
        if page== 1:
            params=str(subjects)
        else:
            params=str(subjects)+'/'+str(page)
        request_url=request_url+params
        #print ('request_url=',request_url)
        self.logger.debug('start request %s', request_url)
        request=scrapy.Request(url=request_url,callback=self.parse_page,meta={'point_id':pids,'page':page})
        request.meta['point_id']=pids
        request.meta['page']=page
        return request

    def parse_page(self,response):
        page=response.meta['page']
        point_id = response.meta['point_id']
        
        
        self.logger.debug('response from point_id=%d,page=%d', point_id,page)

        question_list=response.xpath('//div[@class="seoleft"]//li//a/@href').extract()
        for href in question_list:
            yield scrapy.Request(url=href,callback=self.parse_question_answer,meta={'question_url':href,'point_id':point_id})
        #print ("page=" ,page)
        #print ("q_number=",len(question_list))
            
        self.logger.debug('end parse_question_list')
        #for other pages
        page_list=response.xpath('//div[@class="seopage"]//a/text()').extract()
        total_page=len(page_list)
        #print ("total_page=",total_page)
        if (page==1 and total_page>1):
            for p in range(2,int(total_page)+1):
                #for p in range(2,5):
                self.logger.debug('start page for total_page=%s,page=%s', total_page,p)
                
                yield self.request_page(point_id,p)
        else:
            pass


    def parse_question_answer(self,response):
        question_html=response.xpath('//div[@class="q_mokuai"][@id="q_indexkuai2"]//div[@class="q_bot"][@id]/table').extract_first()

        question_text=' '.join(response.xpath('//div[@class="q_mokuai"][@id="q_indexkuai2"]//table//text()').extract())


        answer_html=response.xpath('//div[@class="q_mokuai"][@id="q_indexkuai3"]//div[@class="q_bot"][@id]/table').extract_first()
        answer_text=' '.join(response.xpath('//div[@class="q_mokuai"][@id]//table//text()').extract())

        point_group = ",".join(response.xpath('//div[@class="secinfo"]//span[@class="secname"]/text()').extract())
    
        question_url =  response.meta['question_url']
        titleId = response.meta['point_id']

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
            item['answer_text']=''
        else:
            item['question_url']=question_url
        if not question_url:
            item['titleId']=''
        else:
            item['titleId']=titleId
        if not point_group:
            item['point_group']=''
        else:
            item['point_group']=point_group



        return item






    