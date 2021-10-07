import os
import pyAesCrypt

BASEDIR = os.path.abspath(os.path.dirname(__file__)) + '/files/'
CRYPT_KEY = os.environ.get('CRYPT_KEY')

def decryption(file: str) -> None:
	"""
	Расшифровка файла
	"""
	buffer_size = 512 * 1024
	pyAesCrypt.decryptFile(str(file), os.path.splitext(file)[0], CRYPT_KEY, buffer_size)
	print(f'[Файл <{get_file_name(file)}>, расшифрован]')
	os.remove(file)


def get_file_name(file) -> str:
	"""
	Получение имени файла, отсечение пути до него
	"""
	file_name, file_type = os.path.splitext(file)
	file_name = file_name.replace(BASEDIR, '')
	return file_name


def files_dir(dir: str) -> None:
	"""
	Получение всех файлов под директории dir
	"""
	for sub_dir in os.listdir(dir):
		path = os.path.join(dir, sub_dir)

		if os.path.isfile(path):  # если найден файл шифруем
			if not get_file_name(path).startswith('.'):
				try:
					decryption(path)
				except Exception as err:
					print(f'[Ошибка при расшифровке файла! ERROR:<{err}>]')

		else:  # иначе ищем файлы в под папке
			files_dir(path)


if __name__ == '__main__':
	if CRYPT_KEY is None:
		print('Не указан ключ для расшифровки')
	else:
		files_dir(BASEDIR)