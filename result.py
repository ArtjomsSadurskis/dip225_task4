import csv
import openpyxl
from selenium import webdriver
import time

# Функция для чтения имен из people.csv
def read_names_from_csv(file_name):
    names = []
    with open(file_name, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Пропускаем заголовок, если он есть
        for row in csv_reader:
            names.append(row[0])  # Предполагается, что полное имя находится в первом столбце
    return names

# Функция для получения кодировки через веб-риск
def get_crc32_encoded_name(name):
    driver = webdriver.Chrome()  # Используйте соответствующий драйвер для вашего браузера
    driver.get('https://emn178.github.io/online-tools/crc32.html')
    
    # Вставляем имя в поле ввода
    input_element = driver.find_element_by_id('input')
    input_element.send_keys(name)
    
    # Нажимаем кнопку для вычисления CRC32
    encode_button = driver.find_element_by_id('calculate')
    encode_button.click()
    
    # Ждем, чтобы страница обработала запрос
    time.sleep(2)
    
    # Получаем результат кодировки
    encoded_result = driver.find_element_by_id('result').get_attribute('value')
    
    driver.quit()  # Закрываем браузер
    return encoded_result

# Функция для чтения зарплаты из salary.xlsx
def read_salary_from_excel(file_name, encoded_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    
    salary = None
    for row in sheet.iter_rows(values_only=True):
        if row[0] == encoded_name:
            salary = row[1]  # Предполагается, что зарплата находится во втором столбце
            break
    
    return salary

# Основная часть программы
csv_file = 'people.csv'
excel_file = 'salary.xlsx'

names = read_names_from_csv(csv_file)

total_salaries = {}
for name in names:
    encoded_name = get_crc32_encoded_name(name)
    salary = read_salary_from_excel(excel_file, encoded_name)
    
    if salary is not None:
        total_salaries[name] = salary

# Вывод результатов
for name, salary in total_salaries.items():
    print(f"Имя: {name}, Зарплата: {salary}")

# Рассчитываем общую сумму зарплат
total_sum = sum(total_salaries.values())
print(f"Общая сумма зарплат: {total_sum}")