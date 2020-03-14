#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import bs4

import csv
import collections

from time import sleep
from random import uniform
from random import choice

import logging

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
	}
url_index = 'https://www.say7.info/cook/'

# логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pr')

#шапка csv файла
headCSV = ['Название', 'Описание', 'Категория', 'Теги', 'Изображение', 'Ингридиенты', 'Контент']

result_tuple = collections.namedtuple('parse_content', headCSV)


class Link(object):
	"""docstring for Client"""
	links = []  # ссылки на страницы с основным контентом
	proxy_list = []  # список прокси адресов

	def __init__(self, count_page=None):
		self.session = requests.Session()
		self.session.headers = headers
		self.count_page = count_page


	def get_html(self, url, proxy=None):
		"""парсит страницу и возвращает ссылки на товары"""
		if proxy:
			proxy = {'http' : 'http://'+proxy}
			logger.debug(proxy['http'])
		res = self.session.get(url, proxies=proxy)
		try:
			res.raise_for_status()
			return res.text
		except Exception as e:
			logger.error('Ошибка при загрузке страницы: ' + str(e))


	def get_links_block(self, html):
		""" получение блока с карточками"""
		soup = bs4.BeautifulSoup(html, 'lxml')
		container = soup.select_one('div.lst').select('li')
		for block in container:
			self.set_links(block)
		logger.debug(f'Нашли {len(self.links)} ссылок на рецепты')


	def set_links(self, block):
		""" получение ссылок просмтра катрочек"""
		block = block.find('a').get('href')
		if not block:
			logger.debug('Не найден элемент')  # проверка существует ли такой элемент
			return
		block = block.replace('//', '')
		block = 'https://' + block
		# добавление ссылки в список
		self.links.append(block)
		

	def read_proxy_list(self):
		"""получить прокси ip из файла"""
		with open('proxy.txt', 'r') as f:
			ip = f.read().split('\n')
		logger.info(f'Загружено {len(ip)} прокси адресов')
		return ip


	def get_random_ip(self, proxy_list:list):
		""" функция выбирает случайный ip """
		ip = choice(self.proxy_list)
		logger.debug(f'Запрос с ip: {ip}')
		return ip


	def f_pause(self, start=0, stop=5):
		""" вызов паузы """
		t = uniform(start, stop)
		logger.debug(f'Пауза {t} секунды')
		sleep(t)


	def run(self):
		""" запуск методов сбора линков для парсинга контента"""
		self.proxy_list.extend(self.read_proxy_list())  # список ip

		for i in range(self.count_page):
			self.f_pause(0, 5)
			ip = self.get_random_ip(self.proxy_list)  # получаем случайный ip
			url = url_index + f'linkz_start-{i}0.html'  # корректируем ссылку 
			html = self.get_html(url_index, ip)
			self.get_links_block(html)
		logger.info(f'Всего получили {len(self.links)} ссылок на рецепты')
		

class Recipe(Link):
	"""docstring for Recipe"""
	result = []  # весь спарсеный контент

	def __init__(self):
		super().__init__()
		Link.__init__(self)


	def add_reciept(self, soup):
		""" добавление полученых данных в именноваааннный кортеж """
		self.result.append(result_tuple(
			self.get_title(soup),
			self.get_description(soup),
			self.get_category(soup),
			self.get_tags(),
			self.get_image(soup),
			self.get_ingridients(soup),
			self.content(soup)
			))
		logger.debug(f'Спарсено {len(self.result)} рецептов')


	def soup(self, html):
		""" инициал bs4 """
		soup = bs4.BeautifulSoup(html, 'lxml')
		block = soup.select_one('div.article.h-recipe')
		return block


	def get_category(self, soup):
		""" получение категории просматриваемой катрочки """
		category = soup.select_one('div.bc')
		if not category or not category.select_one('a.subcat'):
			return 'Не найден элемент'
		return category.select_one('a.subcat').text
	

	def get_tags(self):
		""" получение тегов просматриваемой катрочки """
		tags = 'В разработке'
		return tags


	def get_ingridients(self, block):
		""" получение ингридиентов для просматриваемой катрочки """
		ingredients = block.select_one('div.c8.ingredients')
		if not ingredients:
			return 'Не найжен элемент'
		else:	
			ingredients = ingredients.text.strip().replace('\n', '; ').replace('\xa0', ' ')
			return ingredients


	def get_title(self, block):
		""" получение названия просматриваемой катрочки """
		title = block.select_one('h1')
		if not title:
			return 'Не найден элемент'
		else:
			return title.text


	def get_description(self, block):
		""" получение описания просматриваемой катрочки """
		description = block.select_one('div.p-summary')
		if not description:
			return 'не найден элемент'
		else:
			return description.text.replace('\n', ' ').replace('\xa0', ' ')


	def content(self, block):
		""" получение основного контента (текст | изображение)
		просматриваемой катрочки """
		content_text = []
		content_img = []

		content = block.select('p')
		if not content:
			return 'не найден контент'
		else:
			for p in content:
				content_text.append(self.get_text_content(p))
				content_img.append(self.get_img_content(p))
	
		return content_text, content_img


	def get_img_content(self, p):
		""" получение изображения из p тега контента """
		image = p.find('img')
		if image:
			image = image.get('src').replace('_p.jpg', '_x2.jpg')
			return 'https:' + image
		else:
			return 'None'

		
	def get_text_content(self, p):
		""" получение текста из контента """
		text = p.text.replace('\xa0', '').replace('\n', '')
		if text:
			return text
		else:
			return 'None'
		

	def get_image(self, block):
		""" получение изображений из контента """
		block = block.select('p')[-2]
		image = block.find('img').get('src')
		image = 'https:' + image.replace('_p.jpg', '_x2.jpg')
		return image
		
	def save_to_csv(self):
		""" сохранение скопированных данных в csv файл """
		with open('content.csv', 'w', encoding='utf-8') as f:
			writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
			writer.writerow(headCSV)
			for row in self.result:  # построчное сохранение
				writer.writerow(row)
		logger.info('Файл успешно сохранен!')

	def run(self):
		for url in Link.links:
			# задержка 
			self.f_pause(0, 2)
			# получение случайного ip
			ip = self.get_random_ip(Link.proxy_list)
			# запрос
			html = self.get_html(url, ip)
			soup = self.soup(html)
			# добавление данных 
			self.add_reciept(soup)
		# количество спарсеных данных
		logger.info(f'Всего спарсено {len(self.result)} рецептов')
		# сохранение в csv
		self.save_to_csv()


if __name__ == '__main__':
	parserL = Link(5)
	parserL.run()

	recepts = Recipe()
	recepts.run()




	