import pygame
import random
import pickle
from colour import Color
from colour import make_color_factory, HSL_equivalence, RGB_color_picker

pygame.init()

base = {
    'WIDTH': 800,
    'HEIGHT': 800,
    'SEX': ('M', 'F'),
    'M_MOVEMENT': 4,
    'F_MOVEMENT': 4,
    "FPS": 60,
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "ORGANISM_SIZE": 5,
    "STARTING_POP": 175,
    "MUTATION_RANGE": 1000,
    "MUTATION_1_SELECT": (0, 100),
    "MUTATION_2_SELECT": (500, 525),
    "REPODUCTIVE_AGE": (150, 800),
    "LIFE_EXP": (250, 1000)
}

WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 20)

DRY_TERRAIN = pygame.Rect(base['WIDTH'] // 4,
                          base['HEIGHT']//4,
                          base['WIDTH'] // 2,
                          base['HEIGHT']//2)
p1_genotype = [('A', 'a')]
p2_genotype = [('A', 'a')]

mutations = [('B', 'b'), ('C', 'c'), ('D', 'd'), ('F', 'f'), ('E', 'e')]

infile = open('gen_colours.json', 'rb')
gen_colours = pickle.load(infile)
infile.close()


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

    def divide(self):
        genes = []
        for allele in self.genotype:
            strand = random.randint(0, 1)
            genes.append(allele[strand])
        return genes


def draw_window(organisms):
    WIN.fill(base['BLACK'])
    pygame.draw.rect(WIN, (10, 10, 0), DRY_TERRAIN)
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
    if mutate in range(base['MUTATION_2_SELECT'][0], base['MUTATION_2_SELECT'][1]) and len(child.genotype) > 1:
        child.genotype.remove(child.genotype[-1])
    if [('A', 'a'), ('B', 'B'), ('C', 'c')] == child.genotype:
        child.life_exp = child.life_exp * 1.05
        # child.f_movement = 15
        # child.m_movement = 15
    if ('A', 'A') in child.genotype or ('b', 'b') in child.genotype:
        child.life_exp = child.life_exp * 1.01
        # child.f_movement = 10
        # child.m_movement = 10
    if ('A', 'A') in child.genotype:  # and child.sex == 'F':
        child.location.height = child.location.height * 1
        # child.f_movement = 3
        # child.m_movement = 3

    # if len(child.genotype) == 4:
    #     child.location.height = child.location.height * 2
    #     child.location.width = child.location.width // 2
    # if len(child.genotype) == 5:
    #     child.location.height = child.location.height * 3
    #     child.location.width = child.location.width // 2
    # if len(child.genotype) == 6:
    #     child.location.height = child.location.height * 3
    #     child.location.width = child.location.width // 2

    child.location.x = g.location.x + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                     base['ORGANISM_SIZE'] * 1)
    child.location.y = g.location.y + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                     base['ORGANISM_SIZE'] * 1)
    # if child.location.colliderect(DRY_TERRAIN):
    if ('F', 'F') in child.genotype \
            or ('f', 'f') in child.genotype:

        if child.location.colliderect(DRY_TERRAIN):
            child.f_movement = 2
            child.m_movement = 2
            child.life_exp = 8000
            child.repoductive_age = random.randint(50,150)
            child.location.height = child.location.height * 3
            child.location.width = child.location.width * 2

        else:
            child.life_exp = 5

    return child


def update_organisms(organisms):
    updated_organisms = []
    dead = []
    alive = []
    for og in organisms:
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
        if ('F', 'F') in og.genotype \
                or ('f', 'f') in og.genotype:
            if ('A', 'a') in og.genotype \
                    or ('a', 'A') in og.genotype \
                    or ('A', 'A') in og.genotype:
                og.m_movement = 20
                og.f_movement = 20
            if og.location.colliderect(DRY_TERRAIN) \
                    or ('A', 'a') in og.genotype \
                    or ('a', 'A') in og.genotype:
                pass
            elif og.life_exp > 250:
                og.life_exp = 250
        for g in organisms:
            if g.age >= g.repoductive_age:
                if g.location.colliderect(og.location) \
                        and og.age >= og.repoductive_age and len(og.genotype) == len(g.genotype):
                    g.pollination_count += 1
                    og.pollination_count += 1
                    if len(organisms) > base['STARTING_POP'] * 5:
                        pass
                    else:
                        if len(organisms) > base['STARTING_POP'] * 3:
                            offspring = new_organism(og, g, 2)
                        elif len(organisms) > base['STARTING_POP'] * 4:
                            offspring = new_organism(og, g, 1)
                        else:
                            offspring = new_organism(og, g, 3)
                        # print(len(offspring))
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
    # print(len(alive))
    # print(len(updated_organisms))
    # print("=========")
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
            # new.colour = gen_colours[str(new.genotype)]
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
