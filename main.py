import csv
import re
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Словарь для хранения уникальных контактов
unique_contacts = {}

# Обработка каждой записи
for contact in contacts_list[1:]:  # пропускаем заголовок
    # Обработка ФИО
    fio = " ".join(contact[:3]).strip()  # Объединяем первые три элемента
    parts = fio.split(" ")  # Разделяем на части
    lastname = parts[0]  # Фамилия
    firstname = parts[1] if len(parts) > 1 else ''  # Имя
    surname = parts[2] if len(parts) > 2 else ''  # Отчество

    # Форматирование телефона
    phone = contact[5].strip()
    add_number = None
    if phone:
        # Удаляем все нецифровые символы
        phone_digits = re.sub(r'\D', '', phone)

        # Проверяем наличие добавочного номера
        add_number_match = re.search(r'доб\.\s*(\d+)', phone)
        if add_number_match:
            add_number = add_number_match.group(1)

        # Форматируем номер
        if len(phone_digits) == 11 and phone_digits.startswith('8'):
            phone_digits = '7' + phone_digits[1:]  # Заменяем 8 на 7
        elif len(phone_digits) == 10:
            phone_digits = '7' + phone_digits  # Добавляем 7 для 10-значного номера

        # Приводим к формату +7(999)999-99-99
        phone = f"+7({phone_digits[1:4]}){phone_digits[4:7]}-{phone_digits[7:9]}-{phone_digits[9:11]}"

        # Добавляем добавочный номер, если он есть
        if add_number:
            phone += f" доб.{add_number}"

    # Формируем ключ для уникальности (по ФИО)
    key = (lastname, firstname, surname)

    # Объединяем записи
    if key not in unique_contacts:
        unique_contacts[key] = [lastname, firstname, surname, contact[3], contact[4], phone, contact[6]]
    else:
        existing_contact = unique_contacts[key]
        # Обновляем организацию и должность, если они пустые
        if existing_contact[3] == '':
            existing_contact[3] = contact[3]
        if existing_contact[4] == '':
            existing_contact[4] = contact[4]
        # Обновляем телефон и email, если они пустые
        if existing_contact[5] == '' and phone:
            existing_contact[5] = phone
        if existing_contact[6] == '' and contact[6]:
            existing_contact[6] = contact[6]

# Преобразуем словарь обратно в список
contacts_list = [list(key) + value[3:] for key, value in unique_contacts.items()]

# Добавляем заголовок
contacts_list.insert(0, ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email'])

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
