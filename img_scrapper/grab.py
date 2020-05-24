# -*- coding: utf-8 -*-
"""
Image Gallery - Create an image abstract class and then a class that inherits 
from it for each image type. Put them in a program which displays them in a gallery 
style format for viewing.
"""

import requests
import bs4


class Grab():
	"""docstring for Client"""

	def __init__(self, url):
		self.session = requests.Session()
		self.url = self.url_plus(url)

	def url_plus(self, url):
		""""""
		if url[-1] == '/':
			return url[:-1]
		return url

	def get_page(self):
		"""загрузка страницы"""
		res = ['']
		try:
			res.append(self.session.get(self.url))
			res[1].raise_for_status()
			res[1] = res[1].text
			return res
		except Exception as e:
			res[0] = 'Ошибка при загрузке страницы: ' + str(e)
			return res

	def images(self):
		"""вытаскивание блока из контейнера блоков"""
		page = self.get_page()
		if len(page) > 1:
			soup = bs4.BeautifulSoup(page[1], 'lxml')
			img = [img.get('src') for img in soup.findAll('img')]
			img = [self.url+x if x[0] == '/' else x for x in set(img)]
			return img
		else:
			return page[0]

	def run(self):
		"""запуск функций сбора данных"""
		images = self.images()
		return images


if __name__ == '__main__':
	url = 'http://ods.ai'
	parser = Grab(url)
	images = parser.run()
	print(images)
