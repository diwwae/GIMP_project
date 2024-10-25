#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from gimpfu import *

def create_psd_with_background_and_text(image_path, output_path, text, font="Arial", font_size=30, text_x=50, text_y=50):
    # Открытие JPG как изображение
    image = pdb.gimp_file_load(image_path, image_path)

    # Получаем размеры изображения
    width = pdb.gimp_image_width(image)
    height = pdb.gimp_image_height(image)

    # Создаем новое изображение (PSD) с размерами оригинального изображения
    psd_image = pdb.gimp_image_new(width, height, RGB)

    # Создаем новый слой для фона (копируем слой изображения)
    background_layer = pdb.gimp_layer_new_from_drawable(image.active_layer, psd_image)
    pdb.gimp_image_add_layer(psd_image, background_layer, -1)

    # Добавляем текстовый слой
    text_layer = pdb.gimp_text_layer_new(psd_image, text, font, font_size, 0)
    pdb.gimp_image_add_layer(psd_image, text_layer, -1)

    # Устанавливаем позицию текста
    pdb.gimp_layer_set_offsets(text_layer, text_x, text_y)

    pdb.gimp_file_save(psd_image, background_layer, output_path, output_path)

    # Открываем изображение для просмотра в GIMP
    gimp.Display(psd_image)
    gimp.displays_flush()

    # if (('jpg' or 'jpeg') in output_path):
    #     merged_layer = pdb.gimp_image_merge_visible_layers(psd_image, CLIP_TO_IMAGE)
    #     # Сохраняем результат в формате JPG
    #     pdb.file_jpeg_save(psd_image, merged_layer, output_path, output_path, 0.9, 0, 1, 0, "", 0, 1, 0, 0)
    
    # elif ('png' in output_path):
    #     merged_layer = pdb.gimp_image_merge_visible_layers(psd_image, CLIP_TO_IMAGE)
        
    #     pdb.file_png_save(psd_image, merged_layer, output_path, output_path, 0.9, 0, 1, 0, "", 0, 1, 0, 0)

    # else:
    #     pdb.gimp_file_save(psd_image, background_layer, output_path, output_path)

    # Очистка
    pdb.gimp_image_delete(image)
    return

# Регистрация скрипта в GIMP
register(
    "python_fu_add_text",
    "Создание изображения с фоном и текстом",
    "Берет JPG изображение как фон и добавляет текст с указанием позиции",
    "Your Name", "Your Name", "2024",
    "Создание JPG с текстом...",
    "",  # Типы изображений
    [
        (PF_FILE, "image_path", "Путь к изображению (JPG)", None),
        (PF_STRING, "output_path", "Путь для сохранения", None),
        (PF_STRING, "text", "Текст для добавления", "Пример текста"),
        (PF_FONT, "font", "Шрифт", "Arial"),
        (PF_INT, "font_size", "Размер шрифта", 30),
        (PF_INT, "text_x", "Позиция текста по X", 50),
        (PF_INT, "text_y", "Позиция текста по Y", 50)
    ],
    [],
    create_psd_with_background_and_text,
    menu="<Image>/AddLayer/"
)

main()
