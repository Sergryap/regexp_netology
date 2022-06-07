from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
	rows = csv.reader(f, delimiter=",")
	contacts_list = list(rows)

count_ind = {}
for i, rew in enumerate(contacts_list[1:], start=1):
	name = ' '.join(rew[:2]).split()
	j = 0
	while j < len(name):
		contacts_list[i][j] = name[j]
		j += 1
	# составляем словарь {фамилия: [список из индексов с повторяющимися фамилиями]}
	count_ind[contacts_list[i][0]] = count_ind.get(contacts_list[i][0], []) + [i]
# создаем новый список без дублей:
contacts_list_new = [contacts_list[0]].copy()

for ind in count_ind.values():
	if len(ind) > 1:
		for n, i in enumerate(ind):
			if n == 0:
				s = contacts_list[i].copy()
			else:
				for j in range(len(contacts_list[0])):
					if not s[j]:
						# заменяем пустые значения:
						s[j] = contacts_list[i][j]
	else:
		s = contacts_list[ind[0]].copy()
	contacts_list_new.append(s)

for i, rew in enumerate(contacts_list_new[1:], start=1):
	tel = rew[-2]
	pattern = re.compile(r'[7|8]\s*\(?(\d{,3})\)?\s*-?(\d{,3})-?(\d{,2})-?(\d{,2})\s*\(?(?:\bдоб\b\.?)?\s*(\d*)')
	res = pattern.search(tel)
	tel_delta = f' доб.{res.group(5)}' if res.group(5) else ""
	tel_format = f'+7({res.group(1)}){res.group(2)}-{res.group(3)}-{res.group(4)}{tel_delta}'
	contacts_list_new[i][-2] = tel_format

with open("phonebook.csv", "w", encoding="utf-8") as f:
	datawriter = csv.writer(f, delimiter=',')
	datawriter.writerows(contacts_list_new)

print(contacts_list_new)
