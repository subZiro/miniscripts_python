#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json


BASEDIR = os.path.abspath(os.path.dirname(__file__))
with open(BASEDIR + '/config.json', 'r') as f:
	config_json = json.load(f)

		
class Config:
	"""Конфигурационные параметры преложения"""

	CHROMEDRIVER = BASEDIR + '/chromedriver'  # version in dir 83.0.4103.39
	USER_NAME = config_json['USER_NAME']
	USER_ID = config_json['USER_ID']
	URL_TO_DOCTOR = config_json['URL_TO_DOCTOR']


if __name__ == '__main__':
	print('(-_-)')
