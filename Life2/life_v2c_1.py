import pygame
import random
import pickle
import math
from colour import make_color_factory, HSL_equivalence, RGB_color_picker

pygame.init()


def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


base = {
    'WIDTH': 1280,
    'HEIGHT': 800,
    'SEX': ('M', 'F'),
    'M_MOVEMENT': 3,
    'F_MOVEMENT': 3,
    "FPS": 60,
    "WHITE": (255, 255, 255),
    "BLACK": (75, 75, 75),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "ORGANISM_SIZE": 5,
    "STARTING_POP": 60,
    "MUTATION_RANGE": 1000,
    "MUTATION_1_SELECT": (0, 250),
    "MUTATION_2_SELECT": (500, 750),
}
WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 20)

# p1_genotype = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'd'), ('E', 'E'), ('F', 'F')]
# p2_genotype = [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'D'), ('e', 'e'), ('f', 'f')]

p1_genotype = [('A', 'A')]
p2_genotype = [('a', 'a')]

mutations = [('B', 'b'), ('C', 'c'), ('D', 'd'), ('E', 'e'), ('F', 'f'), ('G', 'g')]

infile = open('gen_colours.json', 'rb')
gen_colours = pickle.load(infile)
infile.close()

DRY_TERRAIN = pygame.Rect(random.randint(0, base['WIDTH']) - 200,
                          random.randint(0, base['HEIGHT']) - 200,
                          200,
                          200)

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
        self.start_location = ()

        self.state = 1
        self.repoductive_age = random.randint(50, 500)
        self.life_exp = random.randint(50, 2500)
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
    # pygame.draw.rect(WIN, (0, 0, 0), DRY_TERRAIN)
    for p in organisms:
        pygame.draw.rect(WIN, p.colour, p.location)
        if len(p.start_location) > 0:
            # print(p.start_location.center)
            pygame.draw.line(WIN, p.colour, p.start_location.center, p.location.center, 1)
    pygame.display.update()


def update_organisms(organisms):
    updated_organisms = []
    dead = []
    alive = []
    rects = []

    for og in organisms:
        if og.age < og.life_exp:
            og.age += 1
        # if og.age >= og.life_exp:
        #     og.state = 0
        if og.pollination_count > 3:
            og.state = 0
        if og.state == 0:
            dead.append(og)
        if og.state == 1:
            alive.append(og)
            rects.append(og.location)

    for og in organisms:
        count = 0
        nearest = {}
        while count == 0:
            for g in organisms:
                if g != og:
                    if og.genotype == g.genotype:
                        # if len(og.genotype) == len(g.genotype):
                        # if og.genotype[1] == g.genotype[1] and og.genotype[2] == g.genotype[2]:
                        bio_1_cx = og.location.centerx
                        bio_1_cy = og.location.centery
                        bio_2_cx = g.location.centerx
                        bio_2_cy = g.location.centery
                        d = math.sqrt(abs(bio_1_cx - bio_2_cx) ** 2 + abs(bio_1_cy - bio_2_cy) ** 2)
                        # if random.randint(250,500) > d > random.randint(25,100):
                        # if random.randint(150,800) > d > 10:
                        if 2000 > d > 350:
                            nearest[d] = g
                count = 1

        try:
            g = nearest[min(nearest.keys())]
            if og.location.x - g.location.x >= 1:
                og.location.x -= random.randint(-2, 3)
            elif og.location.x - g.location.x < 1:
                og.location.x += random.randint(-2, 3)
            if og.location.y - g.location.y >= 1:
                og.location.y -= random.randint(-2, 3)
            elif og.location.y - g.location.y < 1:
                og.location.y += random.randint(-2, 3)
            while og.location.x < 0:
                og.location.x += og.f_movement
            while og.location.x + base['ORGANISM_SIZE'] > base['WIDTH']:
                og.location.x += - og.f_movement
            while og.location.y < 0:
                og.location.y += og.f_movement
            while og.location.y + base['ORGANISM_SIZE'] > base['HEIGHT']:
                og.location.y += -og.f_movement
        except Exception:
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

    for og in organisms:
        if og.location.collidelist(rects):
            rect = og.location.collidelist(rects)
            # print(rect)
            g = alive[rect]
        # for g in organisms:
        try:
            if g.age >= g.repoductive_age:
                if g.location.colliderect(og.location) \
                        and og.age >= og.repoductive_age and len(g.genotype) == len(og.genotype):
                    g.pollination_count += 1
                    og.pollination_count += 1
                    if len(organisms) > base['STARTING_POP'] * 5:
                        pass
                    else:
                        if len(organisms) > base['STARTING_POP'] * 2:
                            offspring = new_organism(og, g, 2)
                        elif len(organisms) > base['STARTING_POP'] * 4:
                            offspring = new_organism(og, g, 1)
                        else:
                            offspring = new_organism(og, g, 2)
                        for child in offspring:
                            child.start_location = og.location
                            mutate = random.randint(0, base['MUTATION_RANGE'])
                            if mutate in range(base['MUTATION_2_SELECT'][0], base['MUTATION_2_SELECT'][1]) and len(
                                    child.genotype) > 1:
                                child.genotype.remove(child.genotype[-1])
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
                            # if [('A', 'a'), ('B', 'B'), ('C', 'c')] == child.genotype:
                            #     child.life_exp = child.life_exp * 1
                            #     child.f_movement = 3
                            #     child.m_movement = 3
                            # if ('A', 'A') in child.genotype and ('b', 'b') in child.genotype:
                            #     child.life_exp = child.life_exp * 1
                            #     child.f_movement = 3
                            #     child.m_movement = 3
                            # if ('A', 'A') in child.genotype:  # and child.sex == 'F':
                            #     child.location.height = child.location.height * 1
                            #     child.f_movement = 3
                            #     child.m_movement = 3
                            # if ('b', 'b') in child.genotype:  # and child.sex == 'F':
                            #     child.location.width = child.location.width * 1
                            child.location.x = g.location.x + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                                             base['ORGANISM_SIZE'] * 1)
                            child.location.y = g.location.y + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                                             base['ORGANISM_SIZE'] * 1)
                            updated_organisms.append(child)
        except Exception as e:
            pass

    for new_og in updated_organisms:
        alive.append(new_og)
    return alive


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
        new.start_location = new.location
        colour = RGB_color_picker(new.genotype)
        rgb = hex_to_rgb(colour.hex)
        new.colour = rgb
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
