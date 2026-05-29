import os
import glob

base = os.path.dirname(os.path.abspath(__file__))

pattern = os.path.join(base, '*', '*', 'settings.py')
files = glob.glob(pattern)

for f in files:
    txt = open(f, encoding='utf-8').read()
    old = "'django.contrib.contenttypes',"
    new = "'django.contrib.contenttypes',\n    'django.contrib.auth',"
    if 'django.contrib.auth' not in txt:
        txt = txt.replace(old, new)
        open(f, 'w', encoding='utf-8').write(txt)
        print('fixed:', f)
    else:
        print('already ok:', f)

print('\nDone! Now run: docker compose down && docker compose up --build')
