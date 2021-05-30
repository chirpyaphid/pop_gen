import pygame
import random
from gen_settings import *
import base_functions as bf

class plant:
    def __init__(self, genotype, name, phenotypes, fem_count):
        self.genotype = genotype
        self.name = name
        self.phenotypes = phenotypes
        self.location = pygame.Rect(random.randint(base['OUTPUT_WIDTH'], base['WIDTH']),
                                    random.randint(0, base['HEIGHT']),
                                    base['P_HEIGHT'],
                                    base['P_WIDTH'])
        if fem_count <= 5:
            self.sex = 'F'
        else:
            self.sex = base['SEX'][random.randint(0, 1)]
        self.state = 'Alive'
        self.life_exp = random.randint(plant_details['m_life_min'], plant_details['m_life_max'])
        self.age = 0
        self.gen = 0
        self.offspring = 0
        self.pollination_count = 0
        self.max_pollination_count = 50
        self.movement = MALE_MOVEMENT

    def divide(self):
        genes = []
        for allele in self.genotype:
            strand = random.randint(0, 1)
            genes.append(allele[strand])
        return genes

    def pheno(self):
        phenotype = []
        colour = bf.colour_pheno(self.genotype)
        for p in self.genotype:
            for key in self.phenotypes['dom'].keys():
                if key in p:
                    phenotype.append(self.phenotypes['dom'][key])
                if p[0] == key.lower() and p[1] == key.lower():
                    phenotype.append(self.phenotypes['res'][key.lower()])
        return phenotype, colour

    def cell(self):
        _, colour = self.pheno()
        return self.location, colour
