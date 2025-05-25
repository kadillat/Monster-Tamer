import pygame
import random
import timer
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
    "Batty":  {"element": "normal", "health": 70},
    "Flare":  {"element": "fire", "health": 60},
    "Groudon":  {"element": "normal", "health": 140},
    "Hornet":  {"element": "normal", "health": 70},
    "Hydro":  {"element": "water", "health": 90},
    "Jelly":  {"element": "water", "health": 65},
    "Kamai":  {"element": "normal", "health": 100},
    "Lorri":  {"element": "normal", "health": 65},
    "Pla":  {"element": "dark", "health": 50},
    "Slyph":  {"element": "ground", "health": 80},
    "Windy":  {"element": "wind", "health": 60},
    "Behemoth":  {"element": "normal", "health": 140},
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
    "scratch": {"damage": random.randint(7,19), "element":"normal", "animation": "scratch"},
    "slash": {"damage": random.randint(10,25), "element":"normal", "animation": "slash"},
    "fireball": {"damage": random.randint(7,19), "element":"fire", "animation": "fire"},
    'splash':  {'damage': random.randint(7,19),  'element': 'water',  'animation': 'splash'},
    'explosion': {'damage': random.randint(10,25),  'element': 'fire',   'animation': 'explosion'},
    "ice shard": {"damage": random.randint(10,25), "element":"water", "animation": "ice"},
    "darkness": {"damage": random.randint(11,29), "element":"dark", "animation": "dark"}


}

element_data = {
    "fire": {"water": 0.5, "normal": 1, "dark": 1, "fire": 0.5, "wind": 1, "ground": 1},
    "water": {"water": 0.5, "normal": 1, "dark": 1, "fire": 1.5, "wind": 1, "ground": 1},
    "dark": {"water": 1, "normal": 1.5, "dark": 1, "fire": 1, "wind": 1, "ground": 1},
    "normal": {"water": 1, "normal": 1, "dark": 1, "fire": 1, "wind": 1, "ground": 1},
    "wind": {"water": 1, "normal": 1, "dark": 1.5, "fire": 1, "wind": 0.5, "ground": 0.5},
    "ground": {"water": 0.5, "normal": 1, "dark": 1, "fire": 1, "wind": 1.5, "ground": 1}
    


}
