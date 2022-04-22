import os
import base64
import pyAesCrypt


BASEDIR = os.path.abspath(os.path.dirname(__file__)) + '/files/'
BUFFER_SIZE = 512 * 1024
CRYPT_KEY = os.environ.get('CRYPT_KEY')


def get_file_name(file) -> str:
	"""
	Получение имени файла, отсечение пути до него
	"""
	file_name, file_type = os.path.splitext(file)
	file_name = file_name.replace(BASEDIR, '')
	return file_name


def decrypt_name(file_name: str) -> None:
	"""
	Расшифровка имени файла
	"""
	file_name_str = str(base64.b64decode(file_name.encode('utf-8').decode("utf-8")))
	file_name_str = file_name_str[2:-1]
	return file_name_str


def decryption(file: str) -> None:
	"""
	Расшифровка файла
	"""
	file_name = get_file_name(file)
	de_file_name = decrypt_name(file_name)
	pyAesCrypt.decryptFile(str(file), f'{BASEDIR}/{de_file_name}', CRYPT_KEY, BUFFER_SIZE)
	print(f'[Файл <{file_name}>, расшифрован в <{de_file_name}>]')
	os.remove(file)


def decrypt_files_dir(dir: str) -> None:
	"""
	Получение всех файлов под директории dir
	"""
	for sub_dir in os.listdir(dir):
		path = os.path.join(dir, sub_dir)

		if os.path.isfile(path): 
			if not get_file_name(path).startswith('.'):			
				try:
					decryption(path)
				except Exception as err:
					print(f'[Ошибка при расшифровке файла! ERROR:<{err}>]')

		else:  # иначе ищем файлы в под папке
			decrypt_files_dir(path)


if __name__ == '__main__':
	if CRYPT_KEY is None:
		print('[Не указан ключ для расшифровки]')
	else:
		decrypt_files_dir(BASEDIR)

