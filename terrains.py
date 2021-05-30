import pygame
from gen_settings import *
import random

DRY_TERRAIN = pygame.Rect(base['WIDTH'] * (random.randint(1,3))*.1 + base["OUTPUT_WIDTH"],
                          base['HEIGHT'] * (random.randint(1,7))*.1,
                          base['WIDTH']*.05,
                          base['HEIGHT'] * .05)

WET_TERRAIN = pygame.Rect(base['WIDTH'] * (random.randint(1,3))*.1 + base["OUTPUT_WIDTH"],
                          base['HEIGHT'] * (random.randint(1,7))*.1,
                          base['WIDTH']* .05,
                          base['HEIGHT'] * .05)

SWAMP = pygame.Rect(base['WIDTH'] * (random.randint(1,4))*.1 + base["OUTPUT_WIDTH"],
                          base['HEIGHT'] * (random.randint(1,7))*.1,
                          base['WIDTH']* .05,
                          base['HEIGHT'] * .05)


terrain_list = [{"type":"dry1","terrain":DRY_TERRAIN},
                {"type":"wet1","terrain":WET_TERRAIN},
                {"type":"swamp","terrain":SWAMP}]

def run_check(plant,phenotypes,type):
    if type == "dry1":
        dry_terrain1(plant,phenotypes)
    if type == "wet1":
        wet_terrain1(plant,phenotypes)
    if type == "swamp":
        wet_terrain1(plant,phenotypes)

def dry_terrain1(plant,phenotypes):
    for gt in plant.genotype:
        check = gt[0] + gt[1]
        if check in phenotypes['codom'].keys():
            for codom in phenotypes['codom'].keys():
                if check == codom:
                    for attrib in phenotypes['codom'][codom].keys():
                        if attrib == 'life_exp':
                            if codom in ['Aa','aA']:
                                plant.life_exp = plant.life_exp *1.1
                            if codom in ['aa']:
                                plant.life_exp = plant.life_exp *1.2


def wet_terrain1(plant,phenotypes):
    for gt in plant.genotype:
        check = gt[0] + gt[1]
        if check in phenotypes['codom'].keys():
            for codom in phenotypes['codom'].keys():
                if check == codom:
                    for attrib in phenotypes['codom'][codom].keys():
                        if attrib == 'life_exp':
                            if codom in ['bB','Bb']:
                                plant.life_exp = plant.life_exp * 1.1
                            if codom in ['bb']:
                                plant.life_exp = plant.life_exp * 1.2

def swamp(plant,phenotypes):
    for gt in plant.genotype:
        check = gt[0] + gt[1]
        if check in phenotypes['codom'].keys():
            for codom in phenotypes['codom'].keys():
                if check == codom:
                    for attrib in phenotypes['codom'][codom].keys():
                        if attrib == 'life_exp':
                            if codom in ['bB','Bb']:
                                plant.life_exp = plant.life_exp * .5
                            if codom in ['bb','aa']:
                                plant.life_exp = plant.life_exp * 1