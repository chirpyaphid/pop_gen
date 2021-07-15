import pygame
import random
import pickle
from colour import Color
from colour import make_color_factory, HSL_equivalence, RGB_color_picker
import math

pygame.init()

base = {
    'WIDTH': 800,
    'HEIGHT': 300,
    'SEX': ('M', 'F'),
    'M_MOVEMENT': 3,
    'F_MOVEMENT': 3,
    "FPS": 60,
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "ORGANISM_SIZE": 8,
    "STARTING_POP": 25,
    "MUTATION_RANGE": 1000,
    "MUTATION_1_SELECT": (0, 20),
    "MUTATION_2_SELECT": (500, 525),
    "REPODUCTIVE_AGE": (10, 350),
    "LIFE_EXP": (50, 450)
}

WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 20)

DRY_TERRAIN = pygame.Rect(base['WIDTH'] // 10,
                          0,
                          base['WIDTH'] // 4,
                          base['HEIGHT'])

WET_TERRAIN = pygame.Rect(base['WIDTH'] // 2 + base['WIDTH'] // 8,
                          0,
                          base['WIDTH'] // 4,
                          base['HEIGHT'])

p1_genotype = [('A', 'A')]
p2_genotype = [('a', 'a')]

mutations = [('B', 'b'), ('C', 'c'), ('D', 'd'), ('E', 'e'), ('F', 'f'), ('G', 'g')]

infile = open('gen_colours.json', 'rb')
gen_colours = pickle.load(infile)
infile.close()


# current_cx = current_rect.centerx
# current_cy = current_rect.centery
#
# for rect in rect_list:
#     cx = rect.centerx
#     cy = rect.centery
#
#     if math.sqrt(abs(current_cx-cx)**2 + abs(current_cy-cy)**2)) < distance:
#         nearest_rect = rect


class organism:
    def __init__(self, genotype, name='', phenotypes=[]):
        self.genotype = genotype
        self.sex = base['SEX'][random.randint(0, 1)]
        self.infect_status = 0
        self.name = name
        self.colour = (0, 0, 0)

        self.phenotypes = phenotypes
        self.location = pygame.Rect(random.randint(0, base['WIDTH']),
                                    random.randint(0, base['HEIGHT']),
                                    base['ORGANISM_SIZE'],
                                    base['ORGANISM_SIZE'])

        self.state = 1
        self.repoductive_age = random.randint(base['REPODUCTIVE_AGE'][0], base['REPODUCTIVE_AGE'][1])
        self.life_exp = random.randint(base['LIFE_EXP'][0], base['LIFE_EXP'][1])
        self.age = 0
        self.gen = 0
        self.offspring = 0
        self.pollination_count = 0
        self.max_pollination_count = 0
        self.max_pollination = random.randint(2, 5)
        self.m_movement = base['M_MOVEMENT']
        self.f_movement = base['F_MOVEMENT']
        self.infected_exposure_count = 0
        self.start_terrain = ''

    def divide(self):
        genes = []
        for allele in self.genotype:
            strand = random.randint(0, 1)
            genes.append(allele[strand])
        return genes


def draw_window(organisms):
    WIN.fill(base['BLACK'])
    pygame.draw.rect(WIN, (50, 0, 0), DRY_TERRAIN)
    pygame.draw.rect(WIN, (0, 0, 50), WET_TERRAIN)
    for p in organisms:
        pygame.draw.rect(WIN, p.colour, p.location)

    pygame.display.update()


def handle_off_spring(child, g):
    mutate = random.randint(0, base['MUTATION_RANGE'])
    if mutate in range(base['MUTATION_1_SELECT'][0], base['MUTATION_1_SELECT'][1]):
        mutation_index = random.randint(0, len(mutations) - 1)
        check_count = 0
        for gene in child.genotype:
            if mutations[mutation_index][0].lower() in gene:
                check_count += 1
            if mutations[mutation_index][0].upper() in gene:
                check_count += 1
        if check_count > 0:
            pass
        else:
            child.genotype.append(mutations[mutation_index])
    # if mutate in range(base['MUTATION_2_SELECT'][0], base['MUTATION_2_SELECT'][1]) and len(child.genotype) > 1:
    #     child.genotype.remove(child.genotype[-1])
    # if [('A', 'a'), ('B', 'B'), ('C', 'c')] == child.genotype:
    #     child.life_exp = child.life_exp * 1.05
    #     # child.f_movement = 15
    #     # child.m_movement = 15
    # if ('A', 'A') in child.genotype or ('b', 'b') in child.genotype:
    #     child.life_exp = child.life_exp * 1.01
    #     # child.f_movement = 10
    #     # child.m_movement = 10
    # if ('A', 'A') in child.genotype:  # and child.sex == 'F':
    #     child.location.height = child.location.height * 1
    #     # child.f_movement = 3
    #     # child.m_movement = 3

    # child.location.height = int(base['ORGANISM_SIZE'] * len(child.genotype))

    child.location.x = g.location.x + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                     base['ORGANISM_SIZE'] * 1)
    child.location.y = g.location.y + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                     base['ORGANISM_SIZE'] * 1)
    if ('F', 'F') in child.genotype:
        if child.location.colliderect(DRY_TERRAIN):
            child.m_movement = 1
            child.f_movement = 1
            child.life_exp = child.life_exp * 1.1
            child.repoductive_age = random.randint(75, 400)
            child.location.height = child.location.height // 2
            child.location.width = child.location.width * 3

        else:
            child.life_exp = random.randint(75, 250)
            pass

    if ('f', 'f') in child.genotype:
        if child.location.colliderect(WET_TERRAIN):
            child.m_movement = 1
            child.f_movement = 1
            child.life_exp = child.life_exp * 1.1
            child.repoductive_age = random.randint(75, 400)
            child.location.width = child.location.width // 2
            child.location.height = child.location.height * 3
        else:
            child.life_exp = random.randint(75, 250)

    return child


def update_organisms(organisms):
    updated_organisms = []
    dead = []
    alive = []
    AA_ORGS = []
    for og in organisms:
        if ('A', 'A') in og.genotype:
            AA_ORGS.append(og.location)
    max_distance = {}
    min_distance = {}
    for og in organisms:
        # distance = 60
        # if ('A', 'A') in og.genotype:
        #     current_cx = og.location.centerx
        #     current_cy = og.location.centery
        #     for rect in AA_ORGS:
        #         cx = rect.centerx
        #         cy = rect.centery
        #         d = math.sqrt(abs(current_cx - cx) ** 2 + abs(current_cy - cy) ** 2)
        #         # print(d)
        #         # print(len(max_distance), min_distance)
            #     if len(max_distance) == 0:
            #         max_distance['d'] = d
            #         max_distance['rect'] = rect
            #     if len(min_distance) == 0:
            #         min_distance['d'] = d
            #         min_distance['rect'] = rect
            #
            #     elif d > max_distance['d']:
            #         max_distance['d'] = d
            #         max_distance['rect'] = rect
            #     elif d < min_distance['d']:
            #         min_distance['d'] = d
            #         min_distance['rect'] = rect
            # print(max_distance, min_distance)

        og.age += 1
        if og.sex == 'F':
            og.location.x += random.randint(-og.f_movement, og.f_movement)
            while og.location.x < 0:
                og.location.x += og.f_movement
            while og.location.x + base['ORGANISM_SIZE'] > base['WIDTH']:
                og.location.x += - og.f_movement

            og.location.y += random.randint(-og.f_movement, og.f_movement)
            while og.location.y < 0:
                og.location.y += og.f_movement
            while og.location.y + base['ORGANISM_SIZE'] > base['HEIGHT']:
                og.location.y += -og.f_movement
        else:
            og.location.x += random.randint(-og.m_movement, og.m_movement)
            while og.location.x < 0:
                og.location.x += og.m_movement
            while og.location.x + base['ORGANISM_SIZE'] > base['WIDTH']:
                og.location.x += - og.m_movement

            og.location.y += random.randint(-og.m_movement, og.m_movement)
            while og.location.y < 0:
                og.location.y += og.m_movement
            while og.location.y + base['ORGANISM_SIZE'] > base['HEIGHT']:
                og.location.y += -og.m_movement

    for og in organisms:
        # if ('F', 'F') in og.genotype \
        #         or ('f', 'f') in og.genotype:
        #     if ('A', 'a') in og.genotype \
        #             or ('a', 'A') in og.genotype \
        #             or ('A', 'A') in og.genotype:
        #         og.m_movement = 5
        #         og.f_movement = 3
        #     if og.location.colliderect(DRY_TERRAIN) \
        #             or ('A', 'a') in og.genotype \
        #             or ('a', 'A') in og.genotype:
        #         pass
        #     elif og.life_exp > 1000:
        #         og.life_exp = random.randint(250, 1000)
        for g in organisms:
            if g.age >= g.repoductive_age:
                if g.location.colliderect(og.location) \
                        and og.age >= og.repoductive_age and len(og.genotype) == len(g.genotype):
                    g.pollination_count += 1
                    og.pollination_count += 1
                    if len(organisms) > base['STARTING_POP'] * 8:
                        pass
                    else:
                        if len(organisms) > base['STARTING_POP'] * 5:
                            offspring = new_organism(og, g, 3)
                        elif len(organisms) > base['STARTING_POP'] * 7:
                            offspring = new_organism(og, g, 1)
                        else:
                            offspring = new_organism(og, g, 4)
                        for child in offspring:
                            child = handle_off_spring(child, g)
                            updated_organisms.append(child)

    for og in organisms:

        if og.age > og.life_exp:
            og.state = 0
        if og.pollination_count > 0:
            og.state = 0
        if og.state == 0:
            dead.append(og)
        if og.state == 1:
            alive.append(og)

    for new_og in updated_organisms:
        alive.append(new_og)
    return alive


def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


def new_organism(p1, p2, number=base['STARTING_POP'], mode='n'):
    offspring = []
    for x in range(number):
        new = organism(
            list(
                zip(
                    p1.divide(),
                    p2.divide()
                )
            )
        )
        if mode == 'i':
            new.location.x = random.randint(0, base['WIDTH'])
            new.location.y = random.randint(0, base['HEIGHT'])
        try:
            colour = RGB_color_picker(new.genotype)
            rgb = hex_to_rgb(colour.hex)
            new.colour = rgb
        except Exception as e:
            pass
        offspring.append(new
                         )
    return offspring


def main():
    clock = pygame.time.Clock()
    run = True
    p1 = organism(p1_genotype)
    p2 = organism(p2_genotype)
    organisms = new_organism(p1, p2)
    while run:
        clock.tick(base['FPS'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    draw_window(organisms)
        organisms = update_organisms(organisms)
        draw_window(organisms)

    pygame.quit()


if __name__ == "__main__":
    main()
