import os
import io
import base64 
import pyAesCrypt


BASEDIR = os.path.abspath(os.path.dirname(__file__)) + '/files/'
BUFFER_SIZE = 512 * 1024
CRYPT_KEY = os.environ.get('CRYPT_KEY')


def get_file_name(file) -> str:
	"""
	Получение имени файла, отсечение пути до него
	"""
	# file_name, file_type = os.path.splitext(file)
	file_name = file.replace(BASEDIR, '')
	return file_name


def encrypt_name(file_name: str) -> None:
	"""
	Шифрование имени файла
	"""
	file_name_byte = str(base64.b64encode(file_name.encode("utf-8")))
	return file_name_byte[2:-1]


def encryption(file: str) -> None:
	"""
	Шифрование файла
	"""
	file_name = get_file_name(file)
	en_file_name = encrypt_name(file_name)
	pyAesCrypt.encryptFile(str(file), f'{BASEDIR}/{en_file_name}.crp', CRYPT_KEY, BUFFER_SIZE)
	print(f'[Файл <{file_name}>, зашифрован в <{en_file_name}>')
	os.remove(file)


def encrypt_files_dir(dir: str) -> None:
	"""
	Получение всех файлов под директории dir
	"""
	for sub_dir in os.listdir(dir):
		path = os.path.join(dir, sub_dir)

		if os.path.isfile(path):  # если найден файл шифруем его 
			if not get_file_name(path).startswith('.'):  # не скрытый файл
				try:
					encryption(path)
				except Exception as err:
					print(f'[Ошибка при шифровании файла! ERROR:<{err}>]')

		else:  # иначе ищем файлы в под папке
			encrypt_files_dir(path)


if __name__ == '__main__':
	if CRYPT_KEY is None:
		print('[Не указан ключ шифрования]')
	else:
		encrypt_files_dir(BASEDIR)
