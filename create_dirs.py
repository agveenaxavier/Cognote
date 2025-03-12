import os

dirs = [
    'static',
    'static/css',
    'static/js',
    'templates',
    'uploads'
]

for dir in dirs:
    os.makedirs(dir, exist_ok=True)
