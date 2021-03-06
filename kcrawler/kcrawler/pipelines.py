# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import MySQLdb

class KcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

# class DuplicatesPipeline(object):

#     def __init__(self):
#         self.ids_seen = set()

#     def process_item(self, item, spider):
#         if item['link'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['id'])
#             return item

class MySQLStorePipeline(object):

  	def __init__(self):
  		self.conn = MySQLdb.connect(host='localhost',user='kerrgo',passwd='123456',db='kerrgo',charset='utf8')
  		self.cursor = self.conn.cursor()
  	def process_item(self,item,spider):
  		try:
  			# self.cursor.execute("""INSERT INTO kerrgo_test (title,link,location,description,source,category) VALUES (%s,%s,%s,%s,%s,%s)""",
  			# 	(item['title'][0],
  			# 	item['location'][0],
  			# 	item['desc'][0],
  			# 	item['source'],
  			# 	item['category']))
			self.cursor.execute("""INSERT INTO kerrgo_test (title,link,location,description,source,category) VALUES (%s,%s,%s,%s,%s,%s)""",
  				(item['title'],item['link'],item['location'],item['desc'],item['source'],item['category']))
  			self.conn.commit()
  		except MySQLdb.Error, e:
  			print "Error %d: %s" %(e.args[0],e.args[1])
  		return item
  		# try:
    # 		self.cursor.execute("INSERT INTO kerrgo_test (title, link,location,description,source,category) VALUES (%s,%s,%s,%s,%s,%s)",
    # 			(item['title'].encode('utf-8'),
    # 				item['link'].encode('utf-8'),
    # 				item['location'].encode('utf-8'),
    # 				item['desc'].encode('utf-8'),
    # 				item['source'].encode('utf-8'),
    # 				item['category'].encode('utf-8')))
    # 	except MySQLdb.Error, e:
    # 		print "Error %d: %s" %(e.args[0],e.args[1])
    # 	return item
    