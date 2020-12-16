# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy_selenium.models import init_db, create_table, Dribbble
from sqlalchemy.orm import sessionmaker

class DribbblePipeline(object):

    def __init__(self):
        engine = init_db()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        dribbble = Dribbble()

        dribbble.name = item['name'][0]
        dribbble.location = item['location'][0]
        session.add(dribbble)
        
        session.commit()
        session.close()



    