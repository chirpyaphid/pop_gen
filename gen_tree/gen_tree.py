import random
import pygame
import collections
import pickle

# FONT = pygame.font.SysFont(None, 20)
try:
    infile = open('gen_colours.json', 'rb')
    gen_colours = pickle.load(infile)
    infile.close()
except Exception as e:
    gen_colours = {}

try:
    infile = open('pheno_colours.json', 'rb')
    pheno_colours = pickle.load(infile)
    infile.close()
except Exception as e:
    pheno_colours = {}

# print(len(gen_colours))

base = {
    "WIDTH": 1800,
    "HEIGHT": 1000,
    "OUTPUT_WIDTH": 0,
    "PLANT_AREA_WIDTH": 0,
    "FPS": 25,
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "P_HEIGHT": 10,
    "P_WIDTH": 20,
    "SEX": ('M', 'F'),
}

pygame.init()
pygame.display.set_caption(f"Sim Window ID: {random.randint(0, 10)}")
WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

males = []
females = []
current_phenos = []
parent_plants = []

gen_list = {}

p1 = [('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'd'),
      ('E', 'e'), ('F', 'f'),('G', 'g'),('L', 'h'),
      ('I', 'i'),('J', 'j'),('K', 'k'),('L', 'l'),
      ('M', 'm'),('N', 'n'),('O', 'o')]

p2 = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'd'),
      ('E', 'e'), ('F', 'f'),('G', 'g'),('L', 'h'),
      ('I', 'i'),('J', 'j'),('K', 'k'),('L', 'l'),
      ('M', 'm'),('N', 'n'),('O', 'o')]

parents = [p1[:5], p2[:5]]

phenotypes = {"dom": {
    "A": "Tall",
    "B": "Broad",
    "C": "Citrus",
    "D": "Green",
    "E": "Pine",
    "F": "THC",
    "G": "5 LF",
    "H": "Spice",
    "I": "10 W",
    "J": "PM R",
    "K": "Dense",
    "L": "Normal L",
    "M": "Normal L",
    "N": "Sandal Wood",
    "O": "CBG",
    "P": "",
    "Q": "",
    "R": "",
    "S": "",
    "T": "",
    "U": "",
    "V": "",
    "W": "",
    "X": "",
    "Y": "",
    "Z": "",
},
    "res": {
        "a": "Short",
        "b": "Narrow",
        "c": "Earthy",
        "d": "Purple",
        "e": "Fuel",
        "f": "CBD",
        "g": "7 LF",
        "h": "Lemon",
        "i": "6 W",
        "j": "BT R",
        "k": "Open",
        "l": "Jagged L",
        "m": "Smooth L",
        "n": "Pepper",
        "o": "THCV",
        "p": "",
        "q": "",
        "r": "",
        "s": "",
        "t": "",
        "u": "",
        "v": "",
        "w": "",
        "x": "",
        "y": "",
        "z": "",
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

off_spring = 10
max_generations = 0


def genotype(genotype):
    global gen_colours
    nc = []
    colour = ()
    if len(gen_colours.keys()) == 0:
        colour = (random.randint(60, 245), random.randint(60, 245), random.randint(60, 245))
        gen_colours[str(genotype[0])] = colour

    if str(genotype[0]) in gen_colours.keys():
        colour = gen_colours[str(genotype[0])]
    else:
        colour = (random.randint(60, 245), random.randint(60, 245), random.randint(60, 245))
        gen_colours.update({str(genotype[0]): colour})
    filename = 'gen_colours.json'
    outfile = open(filename, 'wb')
    pickle.dump(gen_colours, outfile)
    outfile.close()
    return colour


def phenotype_colour(phenotype):
    # print(phenotype)
    global pheno_colours
    nc = []
    colour = ()
    if len(pheno_colours.keys()) == 0:
        colour = (random.randint(60, 245), random.randint(60, 245), random.randint(60, 245))
        pheno_colours[str(phenotype)] = colour

    if str(phenotype) in pheno_colours.keys():
        colour = pheno_colours[str(phenotype)]
    else:
        colour = (random.randint(60, 245), random.randint(60, 245), random.randint(60, 245))
        pheno_colours.update({str(phenotype): colour})
    filename = 'pheno_colours.json'
    outfile = open(filename, 'wb')
    pickle.dump(pheno_colours, outfile)
    outfile.close()
    # print(colour)
    return colour


class plant:
    def __init__(self, genotype, name, phenotypes):
        self.genotype = genotype
        self.name = name
        self.phenotypes = phenotypes
        self.sex = base['SEX'][random.randint(0, 1)]
        self.state = 'Alive'
        self.age = 0
        self.gen = 0
        self.offspring = 0
        self.pollination_count = 0
        self.max_pollination_count = 50
        self.location = pygame.Rect(random.randint(base['OUTPUT_WIDTH'], base['WIDTH']),
                                    50,
                                    base['P_HEIGHT'],
                                    base['P_WIDTH'])

    def divide(self):
        genes = []
        for allele in self.genotype:
            strand = random.randint(0, 1)
            genes.append(allele[strand])
        return genes

    def pheno(self):
        phenotype = []
        # colour = genotype(self.genotype)
        for p in self.genotype:
            for key in self.phenotypes['dom'].keys():
                if key in p:
                    phenotype.append(self.phenotypes['dom'][key])
                if p[0] == key.lower() and p[1] == key.lower():
                    phenotype.append(self.phenotypes['res'][key.lower()])
        colour = phenotype_colour(phenotype)
        return phenotype, colour

    def cell(self):
        _, colour = self.pheno()
        return self.location, colour


def create_next_gen(p1, p2, phenotypes, gen_list):
    global off_spring
    new_plants = []
    gen_next = 0
    off_count = 0
    gen_list[p1.gen + 1] = []
    for x in range(off_spring):
        new_plant = plant(list(zip(p1.divide(),
                                   p2.divide())),
                          f"Plant", phenotypes)
        new_plant.gen = p1.gen + 1

        new_plant.mom_center = p1.location.center
        new_plant.dad_center = p2.location.center

        new_plant.sex = base['SEX'][random.randint(0, 1)]
        gen_0 = 0

        new_plant.location = pygame.Rect(gen_next,
                                         (new_plant.gen + 1) * 50,
                                         base['P_HEIGHT'],
                                         base['P_WIDTH'])
        off_count += 1
        if off_count > off_spring:
            gen_next = 0 + base['P_WIDTH']
            off_count = 0
        else:
            gen_next += base['WIDTH'] // off_spring
        gen_list[new_plant.gen].append(new_plant)
        new_plants.append(new_plant)
    return new_plants


def create_crosses(p1, p2, phenotypes):
    global off_spring
    new_plants = []
    gen_next = 0
    off_count = 0
    for x in range(off_spring):
        new_plant = plant(list(zip(p1.divide(),
                                   p2.divide())),
                          f"Plant", phenotypes)
        new_plant.gen = p1.gen + 1

        new_plant.mom_center = p1.location.center
        new_plant.dad_center = p2.location.center

        new_plant.sex = base['SEX'][random.randint(0, 1)]
        gen_0 = 0

        if new_plant.gen == 0:
            new_plant.location = pygame.Rect(0,
                                             0,
                                             base['P_HEIGHT'],
                                             base['P_WIDTH'])
            gen_0 += 10
        else:
            new_plant.location = pygame.Rect(gen_next,
                                             (new_plant.gen + 1) * 50,
                                             base['P_HEIGHT'],
                                             base['P_WIDTH'])
            off_count += 1
            if off_count > off_spring:
                gen_next = 0 + base['P_WIDTH']
                off_count = 0
            else:
                gen_next += base['WIDTH'] // off_spring

        try:
            gen_list[new_plant.gen].append(new_plant)
            # print(gen_list.keys())
        except Exception as e:
            gen_list[new_plant.gen] = []
            gen_list[new_plant.gen].append(new_plant)
        new_plants.append(new_plant)
    return new_plants


for p in parents:
    parent = plant(p, 'Test', phenotypes)
    parent_plants.append(parent)


def draw_window(plant_list, gen_list, phenotype=[], genotype=[]):
    WIN.fill(BLACK)
    phenotype = FONT.render(f"Phenotype: {phenotype}", True, base['WHITE'])
    WIN.blit(phenotype, [5, 10])
    genotype = FONT.render(f"Genotype: {genotype}", True, base['WHITE'])
    WIN.blit(genotype, [5, 25])
    for p in parent_plants:
        colour = p.cell()[1]
        pygame.draw.rect(WIN, colour, p.location)
    for g in gen_list:
        for p in gen_list[g]:
            colour = p.cell()[1]

            pygame.draw.line(WIN, colour, p.mom_center, tuple([p.location.x, p.location.y]), 1)
            pygame.draw.line(WIN, colour, p.dad_center, tuple([p.location.x, p.location.y]), 1)
            pygame.draw.rect(WIN, colour, p.location)

    pygame.display.update()


parent_plants[0].location.x = base['WIDTH'] * .25
parent_plants[1].location.x = base['WIDTH'] * .75
plant_list = create_crosses(parent_plants[0], parent_plants[1], phenotypes)
x = 1

while max(gen_list.keys()) < max_generations + 1:
    x += 1
    gen_list[x] = []
    try:
        f = random.randint(0, len(gen_list[x - 1]) - 1)
        m = random.randint(0, len(gen_list[x - 1]) - 1)
        while m == f:
            m = random.randint(0, len(gen_list[x - 1]) - 1)
        p1 = gen_list[x - 1][f]
        p2 = gen_list[x - 1][m]
        gen_list[x] = create_crosses(p1, p2,
                                     phenotypes)

    except Exception as e:
        gen_list[x] = create_crosses(gen_list[x - 1][0], gen_list[x - 1][0], phenotypes)


def main():
    global gen_colours, gen_list, plant_list

    clock = pygame.time.Clock()

    run = True
    draw_window(plant_list, gen_list)
    next_gen_parents = []
    while run:
        clock.tick(base['FPS'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    parent_list = list(gen_list.keys())
                    np1 = random.randint(0, off_spring - 1)
                    create_next_gen(gen_list[parent_list[-1]][np1],
                                    gen_list[parent_list[-1]][1],
                                    phenotypes, gen_list)
                    draw_window(plant_list, gen_list)
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_gens = gen_list
                try:
                    for key in active_gens.keys():
                        for plant in active_gens[key]:
                            if plant.location.collidepoint(pygame.mouse.get_pos()):
                                plant.location.width = plant.location.width * 1.5
                                plant.location.height = plant.location.height * 1.5
                                draw_window(plant_list, gen_list)
                                next_gen_parents.append(plant)
                                # print(plant.genotype,plant.pheno())
                                if len(next_gen_parents) == 2:
                                    create_next_gen(next_gen_parents[0],
                                                    next_gen_parents[1],
                                                    phenotypes, gen_list)
                                    draw_window(plant_list, gen_list)
                                    next_gen_parents = []
                        for plant in parent_plants:
                            if plant.location.collidepoint(pygame.mouse.get_pos()):
                                next_gen_parents.append(plant)
                                # print(plant.genotype,plant.pheno())
                                if len(next_gen_parents) == 2:
                                    create_next_gen(next_gen_parents[0],
                                                    next_gen_parents[1],
                                                    phenotypes, gen_list)
                                    draw_window(plant_list, gen_list)
                                    next_gen_parents = []
                except Exception as e:
                    pass
        for key in gen_list.keys():
            for plant in gen_list[key]:
                if plant.location.collidepoint(pygame.mouse.get_pos()):
                    draw_window(plant_list, gen_list, plant.pheno()[0], plant.genotype)
        for plant in parent_plants:
            if plant.location.collidepoint(pygame.mouse.get_pos()):
                draw_window(plant_list, gen_list, plant.pheno()[0], plant.genotype)
    pygame.quit()


if __name__ == "__main__":
    main()
# print(len(create_crosses(parent_plants[0], parent_plants[1], phenotypes)))
