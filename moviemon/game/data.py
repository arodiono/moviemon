from django.conf import settings
import pickle
import random
import requests
import json


class Data:
    def __init__(self):
        self.player_position = settings.PLAYER_POSITION
        self.player_power = 6.5
        self.movieball = 3
        self.moviedex = []
        self.message = ''

    @staticmethod
    def load():
        try:
            with open(settings.DATA_FILE, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            return None

    def dump(self):
        with open(settings.DATA_FILE, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def get_random_movie():
        return settings.MOVIEMONS[random.randint(0, len(settings.MOVIEMONS) - 1)]

    def load_default_settings(self):
        self.player_position = settings.PLAYER_POSITION
        self.player_power = 6.5
        self.movieball = 3
        self.moviedex = []
        self.message = ''

    def get_strength(self):
        pass

    def get_movie(self, movie_id=None):
        if movie_id is None:
            movie_id = self.get_random_movie()

        params = {
            'apikey': 'aa8e8e0',
            'i': movie_id,
            'plot': 'full'
        }
        req = requests.get('http://www.omdbapi.com', params=params)
        return json.loads(req.text)

    def find_movie_or_ball(self):
        if random.random() > 0.85:
            self.find_ball()
            return None
        if random.random() > 0.85:
            return self.find_movie()

    def find_ball(self):
        self.movieball += 1
        self.message = 'You find a movieball!'

    def find_movie(self):
        self.message = 'You find a moviemon! Press A to start catching'
        return self.get_random_movie()
