#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from gimpfu import *
import os

print("\n".join(sys.argv))

def create_psd_with_background_and_text(image_path, text='TEST_TEXT', font="Arial", font_size=30, text_x=50, text_y=50):
    # Распарсим текст, на отдельные сообщения 
    text_array = text.split(' | ')
    
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

    # # Возможные позиции размещения текста
    # positions = [
    #     (width // 2, font_size),                # Верх (по центру горизонтально)
    #     (width // 2, height - 2 * font_size),   # Низ (по центру горизонтально)
    #     (font_size, height // 2),               # Слева (по центру вертикально)
    #     (width - 3 * font_size, height // 2)    # Справа (по центру вертикально)
    # ]


    # По одному добавляем слои текста
    for text in text_array:
        # Добавляем текстовый слой
        text_layer = pdb.gimp_text_layer_new(psd_image, text, font, font_size, 0)
        pdb.gimp_image_add_layer(psd_image, text_layer, -1)

        # Устанавливаем позицию текста
        pdb.gimp_layer_set_offsets(text_layer, text_x, text_y)

    # if (output_path):
        # pdb.gimp_file_save(psd_image, background_layer, image_path, image_path)

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


# def run():
#     image_path = 'popa.jpg'

#     create_psd_with_background_and_text(image_path=image_path)
#     print('asdasdasdasdasds')

    
def run(image_path, text, font, font_size, text_x, text_y):

    create_psd_with_background_and_text(image_path=image_path, text=text, font=font, font_size=font_size, text_x=text_x, text_y=text_y)


# "C:\Program Files\GIMP 2\bin\gimp-2.10.exe" --batch-interpreter python-fu-eval -b "import sys;sys.path=['.']+sys.path;import test;test.run()"
