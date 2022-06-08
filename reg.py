from pprint import pprint
import csv
import re


def reading_session(file_csv: str):
	"""Открытие файла и создание списка"""
	with open(file_csv, encoding="utf-8") as f:
		rows = csv.reader(f, delimiter=",")
		return list(rows)


def name_disposal(book_csv: list):
	"""Расстановка ФИО по своим местам"""
	for i, rew in enumerate(book_csv[1:], start=1):
		name = ' '.join(rew[:2]).split()
		j = 0
		while j < len(name):
			book_csv[i][j] = name[j]
			j += 1
	return book_csv


def merging_duplicates(book_csv: list):
	"""Слияние дубликатов записей"""
	count_ind = {}
	for i, rew in enumerate(book_csv[1:], start=1):
		# составляем словарь {фамилия: [список из индексов с повторяющимися фамилиями]}
		count_ind[book_csv[i][0]] = count_ind.get(book_csv[i][0], []) + [i]
	# создаем новый список без дублей:
	book_csv_new = [book_csv[0]].copy()

	for ind in count_ind.values():
		if len(ind) > 1:
			for n, i in enumerate(ind):
				if n == 0:
					s = book_csv[i].copy()
				else:
					for j in range(len(book_csv[0])):
						if not s[j]:
							# заменяем пустые значения:
							s[j] = book_csv[i][j]
		else:
			s = book_csv[ind[0]].copy()
		book_csv_new.append(s)
	return book_csv_new


def phone_normalizer(book_csv: list):
	"""Форматирование записей телефонов"""
	pattern = re.compile(r'[78]\s*\(?(\d{,3})\)?\s*-?(\d{,3})-?(\d{,2})-?(\d{,2})\s*\(?(?:\bдоб\b\.?)?\s*(\d*)')
	for i, rew in enumerate(book_csv[1:], start=1):
		tel = rew[-2]
		res = pattern.search(tel)
		tel_delta = f' доб.{res.group(5)}' if res.group(5) else ""
		tel_format = f'+7({res.group(1)}){res.group(2)}-{res.group(3)}-{res.group(4)}{tel_delta}'
		book_csv[i][-2] = tel_format
	return book_csv


def phone_normalizer_v1(book_csv: list):
	"""Форматирование записей телефонов. Альтернативный вариант"""
	def u(d: list):
		return "".join(d)

	for i, rew in enumerate(book_csv[1:], start=1):
		tel = rew[-2]
		s = re.findall(r'\d', tel)
		tel_delta = f' доб.{u(s[-4:])}' if len(s) > 11 else ""
		tel_format = f'+7({u(s[1:4])}){u(s[4:7])}-{u(s[7:9])}-{u(s[9:11])}{tel_delta}'
		book_csv[i][-2] = tel_format
	return book_csv


def phone_normalizer_v2(book_csv: list, f='+7(xxx)xxx-xx-xx доб.хххх'):
	"""
	Форматирование записей телефонов.
	Альтернативный вариант с указанием требуемого шаблона
	записи телефона через параметр f
	"""

	for i, rew in enumerate(book_csv[1:], start=1):
		tel = rew[-2]
		s = re.findall(r'\d', tel)

		tel_format = ""
		n = 1
		j = 0
		end_f = re.match(r'[^xXхХ]*', f[::-1])
		while n < len(s) + len(end_f.group()):
			if f[j] in re.findall(r'[^xXхХ]', f):
				tel_format += f[j]
				if n >= len(s):
					n += 1
			else:
				tel_format += s[n]
				n += 1
			j += 1

		book_csv[i][-2] = tel_format
	return book_csv


def writing_to_book_csv(file_csv: str, book_csv: list):
	"""Запись результатов в файл csv"""
	with open(file_csv, "w", encoding="utf-8") as f:
		datawriter = csv.writer(f, delimiter=',')
		datawriter.writerows(book_csv)


if __name__ == '__main__':

	contacts_list = reading_session("phonebook_raw.csv")
	contacts_list = name_disposal(contacts_list)
	contacts_list_new = merging_duplicates(contacts_list)
	# contacts_list_new = phone_normalizer(contacts_list_new)
	contacts_list_new = phone_normalizer_v2(contacts_list_new, f='+7(хxx)xхx-xx-xx доб.xxxx')
	writing_to_book_csv("phonebook.csv", contacts_list_new)
	print(contacts_list_new)
