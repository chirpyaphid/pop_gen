import pygame

MAX_POP = 1000
MALE_MOVEMENT = 20
MALE_SPREAD = 10
FEMALE_SPREAD = 100

base = {
    "WIDTH": 800,
    "HEIGHT": 800,
    "OUTPUT_WIDTH": 0,
    "PLANT_AREA_WIDTH": 0,
    "FINAL_WIDTH": 450,
    "FPS": 60,
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "P_HEIGHT": 4,
    "P_WIDTH": 4,
    "SEX": ('M', 'F'),
    "max_pop": MAX_POP,
    "start_pop": int(MAX_POP * .5),
}

END_BACK = pygame.Rect(0, 0, base['HEIGHT'], base['FINAL_WIDTH'])

p1 = [('A', 'a'), ('b', 'b'), ('C', 'C'), ('D', 'd')]  # , ('E', 'e'), ('F', 'f')]
p2 = [('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'D')]  # , ('E', 'e')]#, ('F', 'f')]

parents = [p1, p2]

phenotypes = {"dom": {
    "A": "Tall",
    "B": "Broad Leaf",
    "C": "Citrus",
    "D": "Green",
    "E": "Pine",
    "F": "THC"
},
    "res": {
        "a": "Short",
        "b": "Narrow Leaf",
        "c": "Earthy",
        "d": "Purple",
        "e": "Fuel",
        "f": "CBD"
    },
    "codom": {
        "BB": {"life_exp": 1.2},
        "AA": {"life_exp": 2},
        "aa": {"life_exp": 1},
        "bb": {"life_exp": 1},
        "aA": {"life_exp": 1},
        "bB": {"life_exp": 1},
        "Aa": {"life_exp": 1},
        "Bb": {"life_exp": 1},
    },
    "linked": {
        "AA": {"height": 2},
        "aa": {"height": 1},
        "bb": {"width": 1},
        "BB": {"width": 3},
    }
}

event_triggers = {
    "pop_trigger1": .50,
    "pop_trigger2": .25,
    "pop_trigger3": .05,
}

plant_details = {
    'm_life_min': 500,
    'm_life_max': 1500,

    'min_males': MAX_POP * .1,
    'male_movement': MALE_MOVEMENT,
    'male_movement_min': MALE_MOVEMENT * -1,

    'male_spread': MALE_SPREAD,
    'male_spread_min': MALE_SPREAD * -1,

    'f_life_min': 500,
    'f_life_max': 5000,
    'mm_age': 50000,

    'female_spread': FEMALE_SPREAD,
    'female_spread_min': FEMALE_SPREAD * -1,

    'max_pollination': 50,
    'death': 0,

    'mutation_point': 150,

}

# Leave these alone
mutation_count = 0
total_males = 0
total_females = 0
max_gen = [0]
max_mom_age = [0]