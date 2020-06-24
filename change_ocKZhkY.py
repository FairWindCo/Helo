#!/usr/bin/env python3.7

import urllib3
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import re


url = "https://nkt.ua/yml_get/kjq8sec8q8p"
http = urllib3.PoolManager()
req = http.request('GET', url)

file_name = 'pricelist.xml'

f = open(file_name, 'wb')
f.write(req.data)
f.close()


#infile = open(file_name, 'r')
#firstLine=''
#secondLine=''
#if infile!=None:
#	firstLine = infile.readline()
#	secondLine = infile.readline()
#	infile.close()
	

tree = ET.ElementTree(file='pricelist.xml')
root = tree.getroot()
#ET.dump(root)

print('Modify Price Elements')
count=0
offers=tree.find('shop/offers')
#ET.dump(offers)
if offers!=None:
	with open('pricelist_new.xml', 'wb') as f:
		for elem in offers.findall('offer'):
			count+=1
			priceelem=elem.find('price')
			if priceelem!=None:
				price = priceelem.text
				newprice = '%.2f' % (float(price.replace(",", ".")) * 1.15,)
				priceelem.text = newprice
			
			name_elem=elem.find('name')
			if name_elem!=None:
				m=re.search("""(Intel|AMD|Ryzen) ([ a-zA-Z0-9\/±+-]+) \((NKT[0-9a-zA-Z-]*|ZBOX[0-9a-zA-Z-]*)\)[ ]*(.*)""",name_elem.text)
				if m!=None:
					obj=m.group(0)
					characters=m.group(1)
					articul=m.group(2)
					other=m.group(4)
					if obj=='Ryzen':
						proc='Ryzen'
					else:
						proc=''
				
					new_name=f"Компьютер {articul} ({proc}{characters}) {other}"
					print(new_name)
					name_elem.text=new_name			
			
			pic_elem=elem.find('picture')
			if pic_elem!=None:
				pic_url = pic_elem.text
				new_pic_url=pic_url.replace("/watermarked/1/","/")
				pic_elem.text=new_pic_url
			
			cat_elem=elem.find('categoryId')
			if cat_elem!=None:
				cat_elem.attrib.clear()
			
			
			newtier = ET.Element("stock_quantity")
			newtier.text=str(10)
			elem.insert(0, newtier)
		print(f'Modified: {count}')	
		#tree.write('price.yml', "UTF-8", True)
		f.write('<?xml version="1.0" encoding="UTF-8" ?>\n<!DOCTYPE yml2_catalog SYSTEM "shops.dtd">\n'.encode('utf8'))
		tree.write(f, "UTF-8")
	#import ftplib
	#with ftplib.FTP('212.113.50.169','techok','TeChOk18$Nkt') as session:
	#	with open('price.yml', 'rb') as f:
	#		session.storbinary('STOR price.yml', f) 
			
else:
	print('No offers found');
	



