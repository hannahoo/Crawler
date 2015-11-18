from scrapy.selector import Selector

f=open('html.txt')
tt=f.read()
#question_html = ['']
#question_html.insert(1,' '.join(Selector(text=tt).xpath('//fieldset[@class="quesborder"]/div[@class="pt1" or @class="pt2"]//*').extract()))
#question_html.insert(2,' '.join(Selector(text=tt).xpath('//fieldset[@class="quesborder"]/div[@class="pt2"]//*').extract()))
#
#question_h = ' '.join(question_html)
#print question_html[2]

question_html='\n'.join(Selector(text=tt).xpath('//fieldset[@class="quesborder"]/div[@class="pt1" or @class="pt2"]//*').extract())

    
question_text='\n'.join(Selector(text=tt).xpath('//fieldset[@class="quesborder"]/div[@class="pt1" or @class="pt2"]//text()').extract())
        
        
answer_html='\n'.join(Selector(text=tt).xpath('//fieldset[@class="quesborder"]/div[@class="pt5" or @class="pt6 per_answer"]//*').extract())
answer_text='\n'.join(Selector(text=tt).xpath('//fieldset[@class="quesborder"]/div[@class="pt5" or @class="pt6 per_answer"]//text()').extract())
question_html=question_html.replace('\r','').replace('\n','')
question_text=question_text.replace('\r','').replace('\n','')
answer_html=answer_html.replace('\r','').replace('\n','')
answer_text=answer_text.replace('\r','').replace('\n','')

print "question_html \n"
print question_html
print "question_text \n"
print question_text
print "answer_text \n"
print answer_text
print "answer_html \n"
print answer_html


#
#test parse
#
#html=Selector(text=tt).xpath('//ul[@class="treeview"]/li/ul/li').extract()
#sec =Selector(text=tt).xpath('//ul[@class="treeview"]/li/ul/li/a/text()').extract()
#        #        print type(html)
#        #        print len(html)
#        
#for i in range(0,len(html)):
#            
#    til = Selector(text=html[i]).xpath('//li/ul/li').extract()
#            
#            #print sec
#    for j in til:
#        title = Selector(text=j).xpath('//a/text()').extract_first()
#        #url = Selector(text=j).xpath('//a/@href').extract_first()
#        title_id = Selector(text=j).xpath('//a/@href').re("\d+")
#        print title
#        #print url
#        print str(title_id[0])
#print sec[i]
# start from page 1 for each title


#test parse_page

#question_list=Selector(text=tt).xpath('//div[@class="content"]//fieldset//span[@class="fieldtip"]/a[1]/@href').extract()
#    
#if (len(question_list)==0):
#    pass
#else:
#    for href in question_list:
#        comp_href='http://www.tiku.cn'+href
#        print comp_href
#                
#                
#    total_page=Selector(text=tt).xpath('//div[@class="seolist"]/a[last()]').re("\d+")
#    print total_page
#    total_page=int(total_page[1])
#    print total_page



