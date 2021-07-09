import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def get_personal():
    img = os.path.join(BASE_DIR, "static/images/person")
    return os.listdir(img)

