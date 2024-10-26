import os
import urllib.request

def download_image(url, output_filename):
    # Скачиваем файл с указанного URL
    response = urllib.request.urlopen(url)
    data = response.read()

    # Сохраняем файл под указанным именем
    with open(output_filename, 'wb') as f:
        f.write(data)
    
    print(f"Файл сохранен как: {output_filename}")

# Пример вызова функции
url = "https://cdn1.ozone.ru/s3/multimedia-1-k/7132820672.jpg"
output_filename = "pics/custom_image.jpg"  # Это имя может передаваться как аргумент в функцию
download_image(url, output_filename)