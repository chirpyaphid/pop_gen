import pygame
MAX_POP = 500
MALE_MOVEMENT = 20
MALE_SPREAD = 10
FEMALE_SPREAD = 100

mutation_count = 0
total_males = 0
total_females = 0
max_gen = [0]
max_mom_age = [0]



base = {
    "WIDTH": 1000,
    "HEIGHT": 1000,
    "OUTPUT_WIDTH": 0,
    "PLANT_AREA_WIDTH": 0,
    "FINAL_WIDTH":450,
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

END_BACK = pygame.Rect(0,0,base['HEIGHT'],base['FINAL_WIDTH'])

event_triggers = {
    "pop_trigger1": .50,
    "pop_trigger2": .25,
    "pop_trigger3": .05,
}

plant_details = {
    'm_life_min': 500,
    'm_life_max': 1500,
    'f_life_min': 500,
    'f_life_max': 5000,
    'mm_age': 50000,
    'min_males': MAX_POP * .4,
    'male_movement': MALE_MOVEMENT,
    'male_movement_min': MALE_MOVEMENT * -1,

    'male_spread': MALE_SPREAD,
    'male_spread_min': MALE_SPREAD * -1,

    'female_spread': FEMALE_SPREAD,
    'female_spread_min': FEMALE_SPREAD * -1,

    'max_pollination': 50,
    'death': 0,

    'mutation_point': 500,

}
