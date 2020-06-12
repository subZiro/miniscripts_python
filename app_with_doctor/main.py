#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from config import Config
 
CHROMEDRIVER = Config.CHROMEDRIVER
URL_TO_DOCTOR = Config.URL_TO_DOCTOR
USER_NAME = Config.USER_NAME
USER_ID = Config.USER_ID


def auth(driver, user, id_user):
	"""Авторизация на сайте"""

	# --ожидание появления всплывающего окна-- #
	driver.implicitly_wait(6) # ждём 6 секунд, по умолчанию - 0
	driver.window_handles 
	# --ввод данных-- #
	name = driver.find_element_by_id('login-f')
	name.send_keys(user)
	user_id = driver.find_element_by_id('login-p')
	user_id.send_keys(id_user)
	# --вход-- #
	btn = driver.find_element_by_id('login-Проверить')
	btn.click()
	# --ожидание авторизации пользователя-- #
	wait = WebDriverWait(driver, 15).until(
		EC.visibility_of_element_located((By.ID,'divlogin')))
	# --завершение авторизации-- #
	connected = driver.find_element_by_css_selector('a').click()
	# --обновление страницы-- #
	sleep(1.3)
	driver.refresh()


def get_btn_to_record(driver):
	"""получение кликабельных конпок для записи"""

	#btn_grey = driver.find_elements(By.TAG_NAME, 'Не активный номерок (откроется в 20.00)')
	#btn_orange = driver.find_elements(By.TAG_NAME, 'Номерок занят')
	btn_all = driver.find_elements_by_css_selector('a.btn.green')
	btn_grey = [elem for elem in btn_all if elem.get_attribute('title') != 'Номерок занят']
	return btn_grey


def get_not_empty_btn(driver, btn_grey):
	"""кликание по всем полученым кнопкам записи"""

	flg = False
	for elem in btn_grey:
		try:
			elem.click()
			alert = driver.switch_to_alert().accept()
		except Exception as e:
			flg = True
			break
	return flg


def record_to_doc(driver):
	"""запись к специалисту"""

	try:
		btn_wait = WebDriverWait(driver, 15).until(
			EC.visibility_of_element_located((By.ID,'zapis-Записаться'))).click()
		# ---- #
		WebDriverWait(driver, 15).until(EC.alert_is_present())
		alert = driver.switch_to_alert().accept()
		return True
	except Exception as e:
		print(e.message)
		return False


def main():
	"""функция запуска всего скрипта"""
	
	driver = webdriver.Chrome(CHROMEDRIVER)
	print(URL_TO_DOCTOR)
	driver.get(URL_TO_DOCTOR)
	#--авторизация--#
	driver.find_element_by_css_selector('a.btn.blue').click()
	auth(driver, USER_NAME, USER_ID)
	# --получение кнопок для записи к специалисту-- #
	all_btn = get_btn_to_record(driver)
	# --если есть свободные места для записи, записываем в первую свободную-- #
	if get_not_empty_btn(driver, all_btn):
		flg_rec = record_to_doc(driver)
		print('Вроде записал, проверяй' if flg_rec else 'Не удалось, давай в следующий раз')
	else:
		print('Нет свободных номерков')
	# --закрытие браузера-- #
	sleep(5)
	driver.quit()


if __name__ == '__main__':
	main()