#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# https://free-proxy-list.net/anonymous-proxy.html
url = 'https://free-proxy-list.net/anonymous-proxy.html'

class Client():

	def __init__(self):
		self.session = requests.Session()
		self.session.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
			'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		}
		self.result = []
		
	def get_html(self, url):
		#получение  html страницы
		res = self.session.get(url)
		try:
			res.raise_for_status()
			return res.text
		except Exception as e:
			print('Ошибка при загрузке страницы: ' + str(e))

	def get_ip_block(self, html):
		# получение блока с ip адресами из страницы
		soup = BeautifulSoup(html, 'lxml')
		container = soup.select_one('tbody').select('tr')
		for block in container:
			self.get_ip(block)

	def get_ip(self, block):
		# вытаскивание из блока адресов связку ip:port
		block = block.select_one('td')
		if not block:
			print('Не найден элемент')  # проверка существует ли такой элемент
			return
		# добавление прокси в конец списка
		self.result.append(f'{block.text.strip()}:{block.next_sibling.text.strip()}')
		
	def save_text(self, list):
		# сохранение в текстовый файл
		file = open('proxy.txt', 'w')
		for elem in list:
			file.write(elem + '\n')
		file.close()
		
	def run(self):
		# запуск сбора ip
		html = self.get_html(url)
		self.get_ip_block(html)
		self.save_text(self.result)


if __name__ == '__main__':
	parser = Client()
	parser.run()