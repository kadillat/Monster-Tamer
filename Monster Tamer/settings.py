import sys
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
os.chdir(script_dir)

import pygame
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



    # Player monsters
monster_data = {
    "Batty": {
        "element": "normal",
        "health": 70,
        "abilities": ["Scratch", "Slash", "Tornado", "Darkness"]
    },
    "Flare": {
        "element": "fire",
        "health": 60,
        "abilities": ["Ember", "Flame burst", "Scratch", "Radiance"]
    },
    "Groudon": {
        "element": "earth",
        "health": 140,
        "abilities": ["Earthquake", "Throw rock", "Tackle", "Slash"]
    },
    "Hornet": {
        "element": "normal",
        "health": 70,
        "abilities": ["Darkness", "Slash", "Tornado", "Tackle"]
    },
    "Hydro": {
        "element": "water",
        "health": 90,
        "abilities": ["Splash", "Tidal wave", "Tackle", "Shock bolt"]
    },
    "Jelly": {
        "element": "water",
        "health": 65,
        "abilities": ["Splash", "Ice shard", "Scratch", "Radiance"]
    },
    "Kamai": {
        "element": "normal",
        "health": 100,
        "abilities": ["Slash", "Scratch", "Throw rock", "Ember"]
    },
    "Lorri": {
        "element": "dark",
        "health": 65,
        "abilities": ["Tackle", "Darkness", "Tornado", "Slash"]
    },
    "Pla": {
        "element": "dark",
        "health": 50,
        "abilities": ["Dark Thunder", "Radiance", "Flame burst", "Scratch"]
    },
    "Slyph": {
        "element": "earth",
        "health": 80,
        "abilities": ["Throw rock", "Earthquake", "Splash", "Tackle"]
    },
    "Windy": {
        "element": "wind",
        "health": 60,
        "abilities": ["Tornado", "Slash", "Shock bolt", "Tackle"]
    },
    "Pav": {
        "element": "dark",
        "health": 60,
        "abilities": ["Shock bolt", "Tackle", "Darkness", "Scratch"]
    },

    "Behemoth": {
        "element": "earth",
        "health": 160,
        "abilities": ["Earthquake", "Throw rock", "Slash", "Tackle"]
    },
    "Cerberus": {
        "element": "fire",
        "health": 150,
        "abilities": ["Ember", "Flame burst", "Scratch", "Darkness"]
    },
    "Crow": {
        "element": "dark",
        "health": 100,
        "abilities": ["Darkness", "Slash", "Tornado", "Tackle"]
    },
    "Garuda": {
        "element": "wind",
        "health": 180,
        "abilities": ["Tornado", "Slash", "Flame burst", "Radiance"]
    },
    "Ghost": {
        "element": "dark",
        "health": 150,
        "abilities": ["Dark Thunder", "Darkness", "Slash", "Shock bolt"]
    },
    "Helm": {
        "element": "normal",
        "health": 150,
        "abilities": ["Tackle", "Scratch", "Throw rock", "Slash"]
    },
    "Keltos": {
        "element": "water",
        "health": 200,
        "abilities": ["Splash", "Tidal wave", "Tackle", "Scratch"]
    },
    "Kraken": {
        "element": "water",
        "health": 120,
        "abilities": ["Splash", "Ice shard", "Darkness", "Tackle"]
    },
    "Reaper": {
        "element": "dark",
        "health": 160,
        "abilities": ["Dark Thunder", "Tornado", "Slash", "Radiance"]
    },
    "Wolvem": {
        "element": "normal",
        "health": 115,
        "abilities": ["Slash", "Tackle", "Darkness", "Flame burst"]
    }
}





ability_data = {
    "Scratch": {"damage": 10, "element":"normal", "animation": "scratch"},
    "Slash": {"damage": 1, "element":"normal", "animation": "slash"},
    "Ember": {"damage": 1, "element":"fire", "animation": "fire"},
    'Splash':  {'damage': 1,  'element': 'water',  'animation': 'splash'},
    'Explosion': {'damage': 1,  'element': 'fire', 'animation': 'explosion'},
    "Ice shard": {"damage": 1, "element":"water", "animation": "ice"},
    "Darkness": {"damage": 1, "element":"dark", "animation": "dark"},
    "Earthquake": {"damage": 1, "element":"earth", "animation": "earth"},
    "Tackle": {"damage": 1 , "element":"normal", "animation": "scratch"},
    "Flame burst": {"damage": 1, "element":"fire", "animation": "fire"},
    "Tidal wave": {"damage": 1, "element":"water", "animation": "splash"},
    "Shock bolt": {"damage": 1, "element":"electric", "animation": "shock"},
    "Radiance": {"damage": 1, "element":"light", "animation": "light"},
    "Throw rock": {"damage": 1, "element":"earth", "animation": "earth"},
    "Tornado": {"damage": 1, "element":"wind", "animation": "wind"},
    "Dark Thunder": {"damage": 1, "element":"dark", "animation": "darkthunder"}


}

element_data = {

    "fire": {"water": 0.5, "normal": 1, "dark": 1.25, "fire": 0.5, "wind": 1.25, "earth": 0.75},
    "water": {"water": 0.5, "normal": 1, "dark": 1, "fire": 1.5, "wind": 1, "earth": 1.5},
    "dark": {"water": 1, "normal": 1.5, "dark": 0.5, "fire": 1, "wind": 1.25, "earth": 1},
    "normal": {"water": 1, "normal": 1, "dark": 1, "fire": 1, "wind": 1, "earth": 1},
    "wind": {"water": 1.25, "normal": 1, "dark": 1.5, "fire": 1, "wind": 0.5, "earth": 0.5},
    "earth": {"water": 0.5, "normal": 1.25, "dark": 1, "fire": 1.25, "wind": 1.5, "earth": 0.75},
    "light": {"dark": 1.5, "normal": 1, "fire": 1, "light": 0.5, "earth": 1, "wind": 1, "water": 1},
    "electric": {"water": 1.5, "earth": 0.5, "normal": 1, "fire": 1, "wind": 1, "dark": 1, "light": 1,}

}
