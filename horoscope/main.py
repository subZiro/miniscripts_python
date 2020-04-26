# -*- coding: utf-8 -*-
# https://goroskop365.ru/
# https://orakul.com/
"""
Fortune Teller (Horoscope) is a program that checks your horoscope in various astrological 
places and collects them for you daily.
"""

import sys
import requests
import bs4


def get_page(url):
	"""загрузка страницы"""
	session = requests.Session()
	res = session.get(url)
	try:
		res.raise_for_status()
		return res.text
	except Exception as e:
		print('Ошибка при загрузке страницы: \n' + str(e))

def get_horoscope(url):
	"""прсит юрл и возвращает гороскоп"""
	page = get_page(url)
	if page:
		soup = bs4.BeautifulSoup(page, 'lxml')
		#получение контейнера с текстом
		container = soup.select_one('div.article__item.article__item_alignment_left.article__item_html').select('p')
		if not container:
			# проверка существования содержимого
			print('гороскоп пуст, попробуйте позже')  
			return
		result = [block.text for block in container]
		result = '\n'.join(result)
		return result

def args(days, signs):
	""""""
	day = 0
	sign = 0

	if len(sys.argv) == 3:
		a, b = sys.argv[1], sys.argv[2]
		# 1 аргумент
		if a.lower() in signs:
			sign = a.lower()
		elif a.lower() in days:
			day = a.lower()
		# 2 аргумент
		if b.lower() in signs:
			sign = b.lower()
		elif b.lower() in days:
			day = b.lower()

	elif len(sys.argv) == 2:
		a = sys.argv[1].lower()
		if a in signs:
			sign = a.lower()
			day = 'сегодня'
	else:
		sign = -1

	return sign, day



def main():
	""""""
	a = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
	b = ['овен', 'телец', 'близнецы', 'рак', 'лев', 'дева', 'весы', 'скорпион', 'стрелец', 'козерог', 'водолей', 'рыбы'] 
	d = {'сегодня' : 'today', 'завтра' : 'tomorrow', 'неделя' : 'week'}
	c = dict(zip(b, a))

	sign, day = args(d, b)
	if sign == '':
		print('не указан знак зодиака')
	elif sign == -1:
		print('Error, не верное количество параметров')
	elif sign == 0:
		print('не верно указан знак зодиака')
	elif day == 0:
		print('не верно указан день')
	else:
		base_url = f'http://horo.mail.ru/prediction/{c[sign]}/{d[day]}/'
		h = get_horoscope(base_url)
		if day == 'неделя':
			day = day[:-1] + 'ю'
		print(f'Гороскоп для {sign} на {day}')
		print(h)


if __name__ == '__main__':
	main()
	print('=' * 30)
