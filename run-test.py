#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os

image_path = sys.argv[1]
text = sys.argv[2]
print("OPENING ", image_path, " WITH ", text)

os.system(f'C:\\"Program Files\"\\"GIMP 2\"\\bin\gimp-2.10.exe --batch-interpreter python-fu-eval -b "import sys;sys.path=[\'.\']+sys.path;import test;test.run(image_path=\'{image_path}\', text=\'{text}\')"')