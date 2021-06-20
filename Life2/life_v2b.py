import pygame
import random
import pickle

pygame.init()

base = {
    'WIDTH': 400,
    'HEIGHT': 400,
    'SEX': ('M', 'F'),
    'M_MOVEMENT': 1,
    'F_MOVEMENT': 1,
    "FPS": 100,
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "ORGANISM_SIZE": 10,
    "STARTING_POP": 100
}
WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 20)

p1_genotype = [('A', 'A'), ('B', 'B'), ('C', 'c')]
p2_genotype = [('A', 'a'), ('b', 'b'), ('C', 'c')]

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
        self.repoductive_age = random.randint(50, 200)
        self.life_exp = random.randint(50, 800)
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
    for p in organisms:
        pygame.draw.rect(WIN, p.colour, p.location)
    pygame.display.update()


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
        for g in organisms:
            if g.age >= g.repoductive_age:
                if g.location.colliderect(og.location) and og.age >= og.repoductive_age:
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
                            if [('A', 'a'), ('B', 'B'), ('C', 'c')] == child.genotype:
                                child.life_exp = child.life_exp * 1.05
                                # child.f_movement = 15
                                # child.m_movement = 15
                            if ('A', 'A') in child.genotype or ('b', 'b') in child.genotype:
                                child.life_exp = child.life_exp * 1.01
                                # child.f_movement = 10
                                # child.m_movement = 10
                            if ('A', 'A') in child.genotype:# and child.sex == 'F':
                                child.location.height = child.location.height * 1
                                # child.f_movement = 3
                                # child.m_movement = 3
                            if ('b', 'b') in child.genotype:# and child.sex == 'F':
                                child.location.width = child.location.width * 1
                            child.location.x = g.location.x + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                                             base['ORGANISM_SIZE'] * 1)
                            child.location.y = g.location.y + random.randint(-base['ORGANISM_SIZE'] * 1,
                                                                             base['ORGANISM_SIZE'] * 1)
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
        new.colour = gen_colours[str(new.genotype)]

        # if [('A', 'a'), ('B', 'B'), ('C', 'c')] == new.genotype:
        #     new.life_exp = new.life_exp * 5
        #     new.repoductive_age = new.repoductive_age * 5
        #     new.location.width = new.location.width * 2
        #     new.f_movement = 0
        #     new.m_movement = 0
        # if ('A', 'a') in new.genotype and ('b', 'b') in new.genotype:
        #     new.life_exp = new.life_exp * 1.1
        #     new.f_movement = 10
        #     new.m_movement = 10
        # if ('A', 'A') in new.genotype:  # and child.sex == 'F':
        #     new.location.height = new.location.height * 1
        #     new.f_movement = 5
        #     # child.m_movement = 10
        # if ('b', 'b') in new.genotype:  # and child.sex == 'F':
        #     new.location.width = new.location.width * 1
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
