from scrapy.selector import Selector

f=open('html.txt')
tt=f.read()
html=Selector(text=tt).xpath('//ul[@id="con_one_1"]/li').extract()
#sec =Selector(text=tt).xpath('//ul[@id="con_one_1"]/li/a/text()').extract()
for i in range(0,len(html)):
    sec = Selector(text=html[i]).xpath('//li[@class]/a/text()').extract_first()
    print sec
    print html[i]
    til = Selector(text=html[i]).xpath('child::*/child::*/child::*/li').extract()
    print len(til)
    print ('til',til)
    for j in til:
        title = Selector(text=j).xpath('//li[1]/a/text()').extract_first()
        url = Selector(text=j).xpath('//li[1]/a/@href').extract_first()
        print title

