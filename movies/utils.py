import os

import requests
from django.conf import settings
from django.utils.text import slugify

OMDB_URL_BASE = 'http://www.omdbapi.com/?apikey'

with open(os.path.join(settings.BASE_DIR, 'omdbapi_key.txt')) as file:
    OMDB_KEY = file.read().strip()

def fetch_movie(title):
    title_slug = slugify(title)
    url = f"{OMDB_URL_BASE}={OMDB_KEY}&t={title_slug}"
    result = requests.get(url)
    raw_dict = result.json()
    return {key.lower(): value for key, value in raw_dict.items()}
   

