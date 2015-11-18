# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from jiaoyu.items import QuestionAnswer
import logging


class JyspiderSpider(scrapy.Spider):
    name = "jyspider2"
    allowed_domains = ["tiku.21cnjy.com/tiku.php"]
    domains="http://tiku.21cnjy.com/tiku.php?mod=quest&channel=6&xd=3"
    start_urls = (
        'http://tiku.21cnjy.com/tiku.php?mod=quest&channel=2&xd=3',

    )
    #channel = 2 --4        6--11

    # chinese math english  physics chemistry history politics geography biology
    # xd =2 junior high xd=3 primary

    def parse(self, response):
        
        
        html=response.xpath('//ul[@id="con_one_1"]/li').extract()
        sec =response.xpath('//ul[@id="con_one_1"]/li/a/text()').extract()
#        print type(html)
#        print len(html)

        for i in range(0,len(html)):
            #print html[i]
            #sec = Selector(text=html[i]).xpath('//li[@class]/a/text()').extract_first()
            #print ('@@@@@@@html',html[i],i)
            #print ('@@@@@@@\n',len(sec),sec[i],i)
            #til = Selector(text=html[i]).xpath('/li[@class]/ul/li').extract()
            til = Selector(text=html[i]).xpath('child::*/child::*/child::*/li').extract()

            #print sec
            for j in til:
                title = Selector(text=j).xpath('//li[1]/a/text()').extract_first()
                url = Selector(text=j).xpath('//li[1]/a/@href').extract_first()
                yield self.request_page(sec[i],title,"http://tiku.21cnjy.com/tiku.php"+url,1)
                
                #title = Selector(text=j).xpath('/li/a/text()').extract_first()
                #url = Selector(text=j).xpath('/li/a/@href').extract()
#                if len(title)!=len(url):
#                    self.logger.debug('error: title number does not match url number for one section\n')
#                for k in range(0,len(title)):
#
#                    yield self.request_page(sec[i],title[k],"http://tiku.21cnjy.com/tiku.php"+url[k],1)

    
    #title = response.xpath('//*[@id="con_one_1"]/li//a/text()')
    #   url = response.xpath('//*[@id="con_one_1"]/li//a/@href')
    
                    


    def request_page(self,section,title,url,page):
        request_url=url
        
        params="&page="+str(page)
        request_url=request_url+params
        #print ('request_url=',request_url)
        self.logger.debug('start request %s', request_url)
        request=scrapy.Request(url=request_url,callback=self.parse_page,dont_filter=True,meta={'page':page,'section':section,'title':title,'url':url})
        request.meta['page']=page
        request.meta['section']=section
        request.meta['title']=title
        request.meta['url']=url
        return request

    def parse_page(self,response):
        page=response.meta['page']
        section=response.meta['section']
        title = response.meta['title']
        url=response.meta['url']
        
        #print ('reponse',response)
        self.logger.debug('response from title=%s,page=%d', title,page)
        

        question_list=response.xpath('//div[@class="questions_col"]//li//a[@class="view_all"]/@href').extract()

        if (len(question_list)==0):
            pass
        else:
            for href in question_list:
                comp_href='http://tiku.21cnjy.com/'+href
                #print ('href=',href)
            
                yield scrapy.Request(url=comp_href,callback=self.parse_question_answer,dont_filter=True,meta={'question_url':comp_href,'title':title,'section':section})
        #print ("page=" ,page)
        #print ("q_number=",len(question_list))
        
            self.logger.debug('end parse_question_list')
        #        #for other pages
        #        page_list=response.xpath('//div[@class="seopage"]//a/text()').extract()
        #        total_page=len(page_list)
        
        
            total_page=response.xpath('//label//span[@title]/@title').re("\d+")
        
            total_page=int(total_page[0])
        
        #print ("total_page=",total_page)
            if (page==1 and total_page>1):
                for p in range(2,int(total_page)+1):
                #for p in range(2,5):
                    self.logger.debug('start page for total_page=%s,page=%s', total_page,p)
                
                    yield self.request_page(section,title,url,p)
            else:
                pass



    def parse_question_answer(self,response):
        question_html=response.xpath('//div[@class="shiti_answer"]//div[@class="answer_detail"]/dl/dt').extract_first()

        question_text=' '.join(response.xpath('//div[@class="shiti_answer"]//div[@class="answer_detail"]/dl/dt//text()').extract())


        answer_html=response.xpath('//div[@class="shiti_answer"]//div[@class="answer_detail"]/dl/dd').extract_first()
        answer_text=' '.join(response.xpath('//div[@class="shiti_answer"]//div[@class="answer_detail"]/dl/dd//text()').extract())
    
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






    