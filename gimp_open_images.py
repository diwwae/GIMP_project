#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем необходимые модули
from gimpfu import *
import os

def open_images_from_paths(image_paths_string):
    # Преобразуем строку с путями в список
    image_paths = image_paths_string.split(',')
    
    for image_path in image_paths:
        image_path = image_path.strip()  # Убираем лишние пробелы
        if os.path.exists(image_path):
            # Открываем изображение в GIMP
            image = pdb.gimp_file_load(image_path, image_path)
            # Обновляем изображение на дисплее
            pdb.gimp_display_new(image)
        else:
            gimp.message("Файл не найден: " + image_path)

# Регистрируем функцию в PDB
register(
          "python-fu-open-images-from-paths",  # Имя регистрируемой функции
          "Открыть изображения",               # Информация о дополнении
          "Открывает несколько изображений в GIMP",  # Краткое описание
          "Ваше Имя",                          # Информация об авторе
          "Ваше Имя",                          # Копирайт
          "2024",                              # Дата создания
          "Открыть изображения",               # Название в меню
          "",                                  # Поддерживаемые типы изображений (можно оставить пустым)
          [
              (PF_STRING, "image_paths_string", "Список путей к изображениям (через запятую)", "")
          ],
          [],                                  # Выходные параметры
          open_images_from_paths,              # Имя основной функции
          menu="<Image>/Custom/")              # Место в меню GIMP

# Запускаем скрипт
main()
