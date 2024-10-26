#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os
import urllib.request

def download_url(url, output_filename):
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


image_path = sys.argv[1]
output_path = sys.argv[2]
image_name = sys.argv[3]
text = sys.argv[4]
font = sys.argv[5]
font_size = sys.argv[6]
text_x = sys.argv[7]
text_y = sys.argv[8]
print("OPENING ", image_path, " WITH ", text)

# Если url-ссылка, то сохраняем
if image_path.startswith("http://") or image_path.startswith("https://"):
    full_output_path = output_path + image_name
    download_url(image_path, full_output_path)

os.system(f'C:\\"Program Files\"\\"GIMP 2\"\\bin\gimp-2.10.exe --batch-interpreter python-fu-eval -b "import sys;sys.path=[\'.\']+sys.path;import test;test.run(image_path=\'{full_output_path}\', text=\'{text}\', font=\'{font}\', font_size=\'{font_size}\', text_x=\'{text_x}\', text_y=\'{text_y}\')"')