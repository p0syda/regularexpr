from pprint import pprint
import csv
import re

# Чтение адресной книги в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Приведение ФИО к единому виду
for contact in contacts_list:
    full_name = ' '.join(contact[:3]).split()
    contact[0] = full_name[0] if len(full_name) > 0 else ''
    contact[1] = full_name[1] if len(full_name) > 1 else ''
    contact[2] = full_name[2] if len(full_name) > 2 else ''

# Приведение номеров телефонов к формату +7(999)999-99-99 доб.9999
phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})(\s*доб\.\s*(\d+))?"
)
phone_substitution = r"+7(\2)\3-\4-\5\6"

for contact in contacts_list:
    contact[5] = phone_pattern.sub(phone_substitution, contact[5])

# Объединение дублирующихся записей
merged_contacts = {}

for contact in contacts_list:
    # Создание ключа по фамилии и имени
    name_key = (contact[0], contact[1])
    if name_key in merged_contacts:
        # Объединение записей, если такой ключ уже существует
        for i in range(2, len(contact)):
            if not merged_contacts[name_key][i]:
                merged_contacts[name_key][i] = contact[i]
    else:
        # Добавление новой записи в словарь
        merged_contacts[name_key] = contact

# Преобразование обратно в список
contacts_list = list(merged_contacts.values())

# Сохранение получившихся данных в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Запись обработанного списка контактов
    datawriter.writerows(contacts_list)

# Вывод результата
pprint(contacts_list)
