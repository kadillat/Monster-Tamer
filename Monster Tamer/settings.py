import pygame
import random
from timer import *
from os.path import join
from os import walk


colors = {
"black": "#000000",
"white": "#ffffff",
"grey": "#808080",
"green": "#008000",
"pink": "#800080",
"red": "#ff0000",
"blue": "#1656ad",
"brown": "#401e12",
"yellow": "#f0c807",
}


monster_data = {
    # Player monsters
    "Batty":  {"element": "normal", "health": 70},
    "Flare":  {"element": "fire", "health": 60},
    "Groudon":  {"element": "normal", "health": 110},
    "Hornet":  {"element": "normal", "health": 70},
    "Hydro":  {"element": "water", "health": 90},
    "Jelly":  {"element": "water", "health": 65},
    "Kamai":  {"element": "normal", "health": 100},
    "Lorri":  {"element": "normal", "health": 65},
    "Pla":  {"element": "dark", "health": 60},
    "Slyph":  {"element": "earth", "health": 80},
    "Windy":  {"element": "wind", "health": 60},
    "Pav":  {"element": "dark", "health": 60},
    # Enemy monsters
    "Behemoth":  {"element": "normal", "health": 130},
    "Cerberus":  {"element": "normal", "health": 120},
    "Crow":  {"element": "normal", "health": 70},
    "Garuda":  {"element": "fire", "health": 120},
    "Ghost":  {"element": "dark", "health": 100},
    "Helm":  {"element": "normal", "health": 120},
    "Keltos":  {"element": "water", "health": 150},
    "Kraken":  {"element": "water", "health": 90},
    "Reaper":  {"element": "dark", "health": 100},
    "Wolvem":  {"element": "normal", "health": 85}
    
}




ability_data = {
    "Scratch": {"damage": random.randint(7,19), "element":"normal", "animation": "scratch"},
    "Slash": {"damage": random.randint(10,25), "element":"normal", "animation": "slash"},
    "Ember": {"damage": random.randint(7,19), "element":"fire", "animation": "fire"},
    'Splash':  {'damage': random.randint(7,19),  'element': 'water',  'animation': 'splash'},
    'Explosion': {'damage': random.randint(10,25),  'element': 'fire', 'animation': 'explosion'},
    "Ice shard": {"damage": random.randint(10,25), "element":"water", "animation": "ice"},
    "Darkness": {"damage": random.randint(11,29), "element":"dark", "animation": "dark"},
    "Earthquake": {"damage": random.randint(11,29), "element":"earth", "animation": "earth"},
    "Tackle": {"damage": random.randint(5,15), "element":"normal", "animation": "scratch"},
    "Flame burst": {"damage": random.randint(12,26), "element":"fire", "animation": "fire"},
    "Tidal wave": {"damage": random.randint(14,28), "element":"water", "animation": "splash"},
    "Shock bolt": {"damage": random.randint(10,24), "element":"electric", "animation": "shock"},
    "Radiance": {"damage": random.randint(8,20), "element":"light", "animation": "light"},
    "Throw rock": {"damage": random.randint(10,22), "element":"earth", "animation": "earth"},
    "Tornado": {"damage": random.randint(9,19), "element":"wind", "animation": "wind"},
    "Dark Thunder": {"damage": random.randint(8,18), "element":"dark", "animation": "darkthunder"}


}

element_data = {

    "fire": {"water": 0.5, "normal": 1, "dark": 1.25, "fire": 0.5, "wind": 1.25, "earth": 0.75},
    "water": {"water": 0.5, "normal": 1, "dark": 1, "fire": 1.5, "wind": 1, "earth": 1.5},
    "dark": {"water": 1, "normal": 1.5, "dark": 0.5, "fire": 1, "wind": 1.25, "earth": 1},
    "normal": {"water": 1, "normal": 1, "dark": 1, "fire": 1, "wind": 1, "earth": 1},
    "wind": {"water": 1.25, "normal": 1, "dark": 1.5, "fire": 1, "wind": 0.5, "earth": 0.5},
    "earth": {"water": 0.5, "normal": 1.25, "dark": 1, "fire": 1.25, "wind": 1.5, "earth": 0.75},
    "light": {"dark": 1.5, "normal": 1, "fire": 1, "light": 0.5, "earth": 1, "wind": 1, "water": 1},
    "electric": {"water": 1.5, "earth": 0.5, "normal": 1, "fire": 1, "wind": 1, "dark": 1}

}
