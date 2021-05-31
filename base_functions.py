import random
from gen_settings import *
from plants import plant
import pickle

try:
    infile = open('gen_colours.json', 'rb')
    gen_colours = pickle.load(infile)
    infile.close()
except Exception as e:
    gen_colours = {}

def colour_pheno(genotype):
    # print(len(gen_colours))
    if str(genotype) in gen_colours.keys():
        colour = gen_colours[str(genotype)]
        pass
    else:
        colour = (random.randint(60, 245), random.randint(60, 245), random.randint(60, 245))
        gen_colours[str(genotype)] = colour
        filename = 'gen_colours.json'
        outfile = open(filename, 'wb')
        pickle.dump(gen_colours, outfile)
        outfile.close()

    return colour

total_males = 0
total_females = 0

def create_crosses(p1, p2, females, males, pollination,phenotypes):
    global mutation_count, total_males, total_females
    if males <= plant_details['min_males']:
        new_plant = plant(list(zip(p1.divide(),
                                   p2.divide())),
                          f"Plant", phenotypes, females)
        new_plant.sex = base['SEX'][random.randint(0, 1)]
    new_plant = plant(list(zip(p1.divide(),
                               p2.divide())),
                      f"Plant", phenotypes, females)
    new_plant.gen = p1.gen + 1

    new_plant.p1_center = p1.location.center
    new_plant.p2_center = p2.location.center

    # Mutation Point
    if new_plant.gen > plant_details['mutation_point']:
        gene_position = random.randint(0, len(new_plant.genotype) - 1)
        new_gene = []
        for allele in new_plant.genotype[gene_position]:
            if allele.isupper():
                new_gene.append(allele.lower())
            else:
                new_gene.append(allele.upper())
        mutation_count += 1
        new_plant.gen = 0
        new_plant.genotype[gene_position] = tuple(new_gene)

    new_plant.sex = base['SEX'][random.randint(0, 1)]

    if pollination == 's':
        new_plant.sex = 'F'
    else:
        if males <= plant_details['min_males']:
            new_plant.sex = 'M'
    if max_gen[0] < new_plant.gen:
        max_gen[0] = (new_plant.gen)
    if new_plant.gen >= plant_details['mutation_point']:
        max_gen[0] = 0
    if new_plant.sex == 'F':
        total_females += 1
    if new_plant.sex == 'M':
        new_plant.location.height = new_plant.location.height // 2
        new_plant.location.width = new_plant.location.width // 2
        total_males += 1
    return new_plant,mutation_count