import os

import requests
from django.utils.text import slugify


OMDB_URL_BASE = 'http://www.omdbapi.com/?apikey'
OMDB_API_KEY = os.environ.get('OMDB_API_KEY')


def fetch_movie(title):
    title_slug = slugify(title)
    url = f"{OMDB_URL_BASE}={OMDB_API_KEY}&t={title_slug}"
    result = requests.get(url)
    raw_dict = result.json()
    return {key.lower(): value for key, value in raw_dict.items()}
