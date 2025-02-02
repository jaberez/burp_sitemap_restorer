#! /usr/bin/python
import sys
import xml.etree.ElementTree as ET
import base64
import subprocess
import re

def decode_base64(data):
   #Декодирует строку из base64.
        return base64.b64decode(data).decode('utf-8')

def parse_xml(file_path):
   #Парсит XML файл и возвращает список элементов <item>.
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root.findall('item')

def extract_json_data(request_data):
    #Извлекает JSON данные из тела запроса, если они есть.
    # Ищем данные в формате {...}
    match = re.search(r'\{.*\}', request_data, re.DOTALL)
    if match:
        json_data = match.group(0).replace('\r\n', '').replace(' ', '')
        return match.group(0)  # Возвращаем найденный JSON
    return None

def build_curl_command(item, new_token):
    #Строит команду curl на основе данных из элемента <item>.
    print("Декодируем поле request")
    request_data = decode_base64(item.find('request').text)

    # Извлекаем метод, путь и хост
    first_line = request_data.splitlines()[0]
    method = first_line.split()[0]
    path = first_line.split()[1]
    host = item.find('host').text

    # Формируем URL
    site_url = f"http://{host}{path}"

   # Извлекаем JSON данные из тела запроса, если они есть
    json_data = extract_json_data(request_data)
    print(json_data)

    # Извлекаем заголовки, исключая Cookie
    headers = {}
    for line in request_data.splitlines()[1:]:
        print(line)
        if line.startswith('Cookie:'):
            continue
        if line.startswith('Content-Length:'):
            continue
        if  "{" in line:
            print("{{{{{{")
            break
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    # Заменяем токен в заголовке Authorization
    if 'Authorization' in headers:
        headers['Authorization'] = f"Bearer {new_token}"


    # Формируем команду curl
    curl_command = ['/usr/bin/curl', '--proxy http://127.0.0.1:8080','-X', method]
    for key, value in headers.items():
        curl_command.extend(['-H', f'"{key}:{value}"'])

    # Если есть JSON данные, добавляем их в команду
#    print(json_data)
    if json_data:
        json_data = f"'{json_data}'"
        curl_command.extend(['-d', json_data])

    curl_command.extend([site_url])
#    print(curl_command)
    return curl_command

def main():
    if len(sys.argv) != 3:
        print("Использование: python script.py <имя_файла.xml> <новый_токен>")
        sys.exit(1)

    file_path = sys.argv[1]
    new_token = sys.argv[2]  # Новый токен из командной строки
    items = parse_xml(file_path)

    for item in items:
  #      print(1)
        curl_command = build_curl_command(item, new_token)
        print(curl_command)
        print("Выполняем команду:", ' '.join(curl_command))

        # Выполняем команду curl
        result = subprocess.run(' '.join(curl_command), capture_output=True, text=True,shell=True)

        # Выводим результат выполнения команды
        print(result.stdout)
        if result.stderr:
            print("Ошибка:", result.stderr)

if __name__ == "__main__":
     print(1)
#     exit
     main()
