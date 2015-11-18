# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionAnswer(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    question_html=scrapy.Field()
    question_text=scrapy.Field()
    answer_html=scrapy.Field()
    answer_text=scrapy.Field()
    question_url=scrapy.Field()
    title = scrapy.Field()
    section = scrapy.Field()


