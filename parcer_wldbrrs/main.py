# -*- coding: utf-8 -*-
"""Wildbeirres parser , result save to csv file"""
import logging  # логгирование
import collections
import csv
import re

import bs4
import requests

import config

# логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

Result_tuple = collections.namedtuple(
	'parse_result', ('brand', 'title', 'price', 'url'),
	)

#шапка csv файла
headCSV = ['Бренд', 'Товар', 'Цена', 'ссылка']

class Client():
	"""docstring for Client"""

	def __init__(self):
		self.session = requests.Session()
		self.session.headers = config.headers
		self.result = []


	def get_page(self, page):
		"""загрузка страницы"""
		url = config.url_parse + '?page=' + str(page)
		res = self.session.get(url)
		try:
			res.raise_for_status()
			return res.text
		except Exception as e:
			logger.error('Ошибка при загрузке страницы: ' + str(e))


	def parse_page(self, text):
		"""парсит страницу и возвращает карточки товаров"""
		soup = bs4.BeautifulSoup(text, 'lxml')
		container = soup.select('div.dtList.i-dtList.j-card-item')
		for block in container:
			self.parse_block(block)


	def parse_block(self, block):
		"""вытаскивание блока из контейнера блоков"""
		# получение блока с сылкой
		url_block = block.select_one('a.ref_goods_n_p')
		if not url_block:
			logger.error('not url block')  # проверка существует ли такой блок
			return
		# получение ссылки на элемент
		url_elem = url_block.get('href')
		if not url_elem:
			logger.error('not url href')  # проверка существует ссылка на элемент
			return
		# получение блока с названием и брендом
		brandname_block = block.select_one('div.dtlist-inner-brand-name')
		if not brandname_block:
			logger.error(f'not block on {url_elem}')  # проверка существует ли такой блок
			return
		# получение блока с именем бренда
		brand_elem = brandname_block.select_one('strong.brand-name')
		if not brand_elem:
			logger.error(f'not brand name on {url_elem}')  # проверка существует ли название бренда
			return
		brand_elem = brand_elem.text.replace('/', '').strip()  # очистка строки
		# получение названия товара
		title_elem = brandname_block.select_one('span.goods-name')
		if not title_elem:
			logger.error('not element name')  # проверка существует ли элемент
			return
		title_elem = title_elem.text.replace('/', '').strip()  # очистка строки
		# получение цены на товар
		price_elem = block.select_one('span.price')
		if not price_elem:
			logger.error('not price element')  # проверка существует блок с ценой
			return

		# очистка строки
		price_elem = price_elem.text.replace('\xa0', '').strip()
		price_elem = price_elem.split('₽')

		self.result.append(Result_tuple(brand_elem, title_elem, price_elem[0], url_elem))

		logger.debug(f'{brand_elem},')
		logger.debug(f'{title_elem}')
		logger.debug(f'{url_elem}') 
		logger.debug('_' * 88)  # форматирование вывода


	def save_to_csv(self):
		"""сохранение в csv файл в папку с проектом"""
		with open('parse.csv', 'w', encoding='cp1251') as f:
			writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
			writer.writerow(headCSV)
			for elem in self.result:
				writer.writerow(elem)


	def run(self):
		"""запуск функций сбора данных"""
		for page in range(1,88):
			text = self.get_page(str(page))
			if text:
				self.parse_page(text)
				logger.info(f'получили {len(self.result)} элементов')
			else:
				break
		self.save_to_csv()


if __name__ == '__main__':
	parser = Client()
	parser.run()