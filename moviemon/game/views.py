from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from .data import Data
import pickle, glob, os, random
import json
from collections import deque


def index(request):
    title = 'MOVIEMON'
    controls = {
        'a': {
            'action': '/worldmap/',
            'params': 'reset'
        },
        'b': {
            'action': '/options/load_game/'
        },
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'start': False,
        'select': False,
    }
    return render(request, 'title.html', locals())


def worldmap(request):
    title = 'Worldmap'

    controls = {
        'a': False,
        'b': False,
        'up': {
            'action': '/worldmap/',
            'params': 'up'
        },
        'down': {
            'action': '/worldmap/',
            'params': 'down'
        },
        'left': {
            'action': '/worldmap/',
            'params': 'left'
        },
        'right': {
            'action': '/worldmap/',
            'params': 'right'
        },
        'select': {
            'action': '/moviedex/'
        },
        'start': {
            'action': '/options/'
        }
    }

    param = request.POST.get('param', False)

    if param == 'reset':
        data = Data()
    else:
        data = Data.load()

    if data is None:
        data = Data()
        data.load_default_settings()

    if request.method == 'POST':
        data.message = ''
    f = None
    if param == 'up' and data.player_position['y'] > 0:
        data.player_position['y'] -= 1
        f = data.find_movie_or_ball()
    elif param == 'down' and data.player_position['y'] < settings.MAP_SIZE['y'] - 1:
        data.player_position['y'] += 1
        f = data.find_movie_or_ball()
    elif param == 'left' and data.player_position['x'] > 0:
        data.player_position['x'] -= 1
        f = data.find_movie_or_ball()
    elif param == 'right' and data.player_position['x'] < settings.MAP_SIZE['x'] - 1:
        data.player_position['x'] += 1
        f = data.find_movie_or_ball()
    else:
        pass

    data.dump()

    if f is None and param in ['up', 'down', 'left', 'right']:
        return redirect('/worldmap/')

    if f is not None:
        controls['a'] = {
            'action': '/battle/' + f,
        }

    return render(request, 'worldmap.html', locals())


def options(request):
    title = 'Options'
    controls = {
        'a': {
            'action': 'save_game/'
        },
        'b': {
            'action': '/'
        },
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'start': {
            'action': '/worldmap/'
        },
        'select': False,
    }
    return render(request, 'options.html', locals())


def moviedex(request):
    title = 'Moviedex'

    data = Data.load()
    if data is None:
        data = Data()
        data.load_default_settings()

    # param = request.POST.get('param', False)
    param = int(request.POST['param']) if request.POST['param'] else 0
    p_next = int(param) + 1
    if p_next < 0:
        p_next = 0
    p_prev = int(param) - 1
    if p_prev < 0:
        p_prev = 0
    i = 0
    controls = {
        'a': {
            "action": '/moviedex/'
        },
        'b': False,
        'up': False,
        'down': False,
        'left': {
            'action': '/moviedex/',
            'params': str(p_prev)
        },
        'right': {
            'action': '/moviedex/',
            'params': str(p_next)
        },
        'start': False,
        'select': {
            'action': '/worldmap/'
        }
    }
    i = 0
    for item in data.moviedex:
        if i == int(param):
            controls["a"]["action"] = '/moviedex/' + item["imdbID"]
        i += 1
    moviedexes = enumerate(data.moviedex)
    return render(request, 'moviedex.html', locals())


def detail(request, movie_id):
    title = 'Detail'
    controls = {
        'a': False,
        'b': {
            'action': '/moviedex/'
        },
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'start': False,
        'select': False,
    }
    data = Data()
    movie = data.get_movie(movie_id)
    return render(request, 'detail.html', locals())


def battle(request, movie_id):
    title = 'Battle'
    controls = {
        'a': {
            'action': '/battle/' + movie_id,
            'params': 'throw'
        },
        'b': {
            'action': '/worldmap/'
        },
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'start': False,
        'select': False,
    }
    data = Data().load()
    data.message = ''
    param = request.POST.get('param', False)
    movie = data.get_movie(movie_id)
    chance = int(50 - (float(movie['imdbRating']) * 10) + (data.player_power * 5))
    if chance > 90:
        chance = 90
    elif chance < 1:
        chance = 1

    if param == 'throw' and data.movieball > 0:
        data.movieball = data.movieball - 1
        if random.randint(0, 100) <= int(chance):
            data.moviedex.append(movie)
            data.message = 'You catched it!'
            controls['a'] = False
        else:
            data.message = 'You missed!'
    data.dump()
    return render(request, 'battle.html', locals())


def options_save(request):
    title = 'Save'
    controls = {
        'a': {
            'action': '/options/save_game/',
            'params': 'save'
        },
        'b': {
            'action': '/options/'
        },
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'start': False,
        'select': False,
    }

    if request.POST.get('param', False) == 'save':
        data = Data().load()
        res = len(data.moviedex)
        with open('slot_' + str(res) + '.nmg', 'wb') as file:
            pickle.dump(data, file)

    return render(request, 'save.html', locals())


def options_load(request):
    title = 'Load'
    controls = {
        'a': {
            'action': '/options/load_game/',
            'params': 'load'
        },
        'b': {
            'action': '/'
        },
        'up': False,
        'down': False,
        'left': False,
        'right': False,
        'start': False,
        'select': False,
    }
    if request.POST.get('param', False) == 'load':
        pass
        # os.getcwd()
        # for file in glob.glob("slot_*"):
        #     f = open(file, 'wb')
        #     Data().load(f.read())

    return render(request, 'load.html', locals())
