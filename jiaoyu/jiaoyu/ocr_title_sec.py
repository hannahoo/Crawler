import scrapy
import json
from scrapy.selector import Selector
import csv

f=open('id1.txt')
content = f.readline()
ocr_title=csv.writer(open('ocr_title','wb'))
ocr_title.writerow(['title','title_id','section_id','grade_id','subject_id','term_id'])
ocr_section=csv.writer(open('ocr_section','wb'))
ocr_section.writerow(['section','section_id','grade_id','subject_id','term_id'])

# oneline for one subject at one term
while(content):
    grade_id=Selector(text=content).xpath('//grade/@id').extract_first()
    term_id=Selector(text=content).xpath('//term/@id').extract_first()
    subject_id=Selector(text=content).xpath('//subject/@id').extract_first()
    section_id='0'

#title
    title_id = Selector(text=content).xpath('//span[@id and @style]/@id').re("\d+")
    title_id = [x for x in title_id if x != '0']
    
    j=0
#    if (len(title_id)!=len(title)):
#        if(title[j].encode('utf-8')==' '):

    for i in range(0,len(title_id)):

        if(title[j].encode('utf-8')==' '):
            j=i+1
        ocr_title.writerow([title[j].encode('utf-8'),title_id[i].encode('utf-8'),section_id.encode('utf-8'),grade_id.encode('utf-8'),subject_id.encode('utf-8'),term_id.encode('utf-8')])
        j=j+1
#section

    section = Selector(text=content).xpath('//h4/text()').extract()

    for i in range(0,len(section)):
        ocr_section.writerow([section[i].encode('utf-8'),i,grade_id.encode('utf-8'),subject_id.encode('utf-8'),term_id.encode('utf-8')])

    content=f.readline()









