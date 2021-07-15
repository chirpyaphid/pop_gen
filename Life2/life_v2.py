import pygame
import random
import pickle

pygame.init()

base = {
    'WIDTH': 1400,
    'HEIGHT': 1000,
    'SEX': ('M', 'F'),
    'MOVEMENT': 10,
    "FPS": 60,
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "ORGANISM_SIZE": 6,
    "STARTING_POP": 200
}
WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 20)

p1_genotype = [('A', 'A'), ('B', 'B') , ('C', 'c')]
p2_genotype = [('A', 'a'), ('b', 'b') , ('C', 'c')]

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
        self.repoductive_age = 400
        self.life_exp = random.randint(600, 650)
        self.age = 0
        self.gen = 0
        self.offspring = 0
        self.pollination_count = 0
        self.max_pollination_count = 0
        self.max_pollination = 5
        self.movement = base['MOVEMENT']
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
            pass
        else:
            og.location.x += random.randint(-og.movement, og.movement)
            while og.location.x < 0:
                og.location.x += og.movement
            while og.location.x + base['ORGANISM_SIZE'] > base['WIDTH']:
                og.location.x += - og.movement

            og.location.y += random.randint(-og.movement, og.movement)
            while og.location.y < 0:
                og.location.y += og.movement
            while og.location.y + base['ORGANISM_SIZE'] > base['HEIGHT']:
                og.location.y += -og.movement

    for og in organisms:
        if og.sex == 'M':
            for g in organisms:
                if g.sex == 'F':
                    if g.age > g.repoductive_age:
                        if g.location.colliderect(og.location):
                            g.pollination_count += 2
                            og.state = 0
                            # g.state = 0
                            if len(organisms) >base['STARTING_POP'] * 15:
                                pass
                            else:
                                if len(organisms) > base['STARTING_POP'] * 3:
                                    offspring = new_organism(og, g, 2)
                                elif len(organisms) > base['STARTING_POP'] * 5:
                                    offspring = new_organism(og, g, 1)
                                else:
                                    offspring = new_organism(og, g, 4)
                                # print(len(offspring))
                                for child in offspring:
                                    if ('A', 'a') in child.genotype and ('b', 'b') in child.genotype:
                                        child.life_exp = child.life_exp * 1.1
                                    if ('a', 'a') in child.genotype and child.sex == 'F':
                                        child.location.height = child.location.height * 2
                                    if ('b', 'b') in child.genotype and child.sex == 'F':
                                        child.location.width = child.location.width * 2
                                    child.location.x = g.location.x + random.randint(-base['MOVEMENT']*15,
                                                                                     base['MOVEMENT']*15)
                                    child.location.y = g.location.y + random.randint(-base['MOVEMENT']*15,
                                                                                     base['MOVEMENT']*15)
                                    updated_organisms.append(child)

    for og in organisms:

        if og.age > og.life_exp:
            og.state = 0
        if og.pollination_count > 5:
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
