import pygame
from gen_settings import *
import random

DRY_TERRAIN = pygame.Rect(random.randint(base['OUTPUT_WIDTH'], base['WIDTH']) - base['P_WIDTH'],
                          random.randint(0, base['HEIGHT']) - base['P_HEIGHT'],
                          base['OUTPUT_WIDTH'] * (random.randint(10, 50)) * .01 - base['P_WIDTH'],
                          base['HEIGHT'] * (random.randint(10, 25)) * .01 - base['P_HEIGHT'])

WET_TERRAIN = pygame.Rect(random.randint(base['OUTPUT_WIDTH'], base['WIDTH']) - base['P_WIDTH'],
                          random.randint(0, base['HEIGHT']) - base['P_HEIGHT'],
                          base['OUTPUT_WIDTH'] * (random.randint(10, 50)) * .01 - base['P_WIDTH'],
                          base['HEIGHT'] * (random.randint(10, 25)) * .01 - base['P_HEIGHT'])

SWAMP = pygame.Rect(random.randint(base['OUTPUT_WIDTH'], base['WIDTH']) - base['P_WIDTH'],
                    random.randint(0, base['HEIGHT']) - base['P_HEIGHT'],
                    base['OUTPUT_WIDTH'] * (random.randint(10, 50)) * .01 - base['P_WIDTH'],
                    base['HEIGHT'] * (random.randint(10, 25)) * .01 - base['P_HEIGHT'])

DRY_TERRAIN2 = pygame.Rect(0, 0, 0, 0)

terrain_list = [{"type":"dry2","terrain":DRY_TERRAIN2}]
# terrain_list = [{"type": "dry1", "terrain": DRY_TERRAIN},
#                 {"type": "wet1", "terrain": WET_TERRAIN},
#                 {"type": "swamp", "terrain": SWAMP}]


def run_check(plant, phenotypes, type):
    if len(terrain_list) == 0:
        pass
    else:
        if type == "dry1":
            dry_terrain1(plant, phenotypes)
        if type == "wet1":
            wet_terrain1(plant, phenotypes)
        if type == "swamp":
            swamp(plant, phenotypes)
        if type == "dry2":
            pass


def dry_terrain1(plant, phenotypes):
    for gt in plant.genotype:
        check = gt[0] + gt[1]
        if check in phenotypes['codom'].keys():
            for codom in phenotypes['codom'].keys():
                if check == codom:
                    for attrib in phenotypes['codom'][codom].keys():
                        if attrib == 'life_exp':
                            if ('a', 'a') in plant.genotype and ('B', 'B') in plant.genotype:
                                plant.life_exp = plant.life_exp * 1.1
                            if ('A', 'A') in plant.genotype:
                                plant.life_exp = plant.life_exp * .95


def wet_terrain1(plant, phenotypes):
    for gt in plant.genotype:
        check = gt[0] + gt[1]
        if check in phenotypes['codom'].keys():
            for codom in phenotypes['codom'].keys():
                if check == codom:
                    for attrib in phenotypes['codom'][codom].keys():
                        if attrib == 'life_exp':
                            if ('A', 'a') in plant.genotype or ('a', 'A') in plant.genotype:
                                plant.life_exp = plant.life_exp * 1.02
                            if ('b', 'b') in plant.genotype:
                                plant.life_exp = plant.life_exp * 1.02
                            if ('A', 'A') in plant.genotype:
                                plant.life_exp = plant.life_exp * .95


def swamp(plant, phenotypes):
    for gt in plant.genotype:
        check = gt[0] + gt[1]
        if check in phenotypes['codom'].keys():
            for codom in phenotypes['codom'].keys():
                if check == codom:
                    for attrib in phenotypes['codom'][codom].keys():
                        if attrib == 'life_exp':
                            if ('A', 'a') in plant.genotype:
                                plant.life_exp = plant.life_exp * 1.05
                            if ('A', 'A') in plant.genotype and ('b', 'b') in plant.genotype:
                                plant.life_exp = plant.life_exp * 1.01
