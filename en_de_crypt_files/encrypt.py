import os
import pyAesCrypt

BASEDIR = os.path.abspath(os.path.dirname(__file__)) + '/files/'
CRYPT_KEY = os.environ.get('CRYPT_KEY')

def encryption(file: str) -> None:
	"""
	Шифрование файла
	"""
	buffer_size = 512 * 1024
	pyAesCrypt.encryptFile(str(file), str(file) + '.crp', CRYPT_KEY, buffer_size)
	print(f'[Файл <{get_file_name(file)}>, зашифрован]')
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

		if os.path.isfile(path):  # если найден файл шифруем его
			if not get_file_name(path).startswith('.'):  # не скрытый файл
				try:
					encryption(path)
				except Exception as err:
					print(f'[Ошибка при шифровании файла! ERROR:<{err}>]')

		else:  # иначе ищем файлы в под папке
			files_dir(path)


if __name__ == '__main__':
	if CRYPT_KEY is None:
		print('Не указан ключ шифрования')
	else:
		files_dir(BASEDIR)