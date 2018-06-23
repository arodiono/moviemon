from django.conf import settings
import pickle
import random
import requests
import json


class Data:
    def __init__(self):
        self.player_position = settings.PLAYER_POSITION
        self.balls_count = 3
        self.movies_catch = []

    def load(self):
        with open(settings.DATA_FILE, 'rb') as file:
            return pickle.load(file)

    def dump(self):
        with open(settings.DATA_FILE, 'wb') as file:
            pickle.dump(self, file)

    def get_random_movie(self):
        return settings.MOVIEMONS[random.randint(0, len(settings.MOVIEMONS))]

    def load_default_settings(self):
        pass

    def get_strength(self):
        pass

    def get_movie(self, movie_id=None):
        if movie_id is None:
            movie_id = self.get_random_movie()

        params = {
            'i': movie_id,
            'plot': 'full'
        }
        req = requests.get('http://www.omdbapi.com', params=params)
        return json.loads(req)
