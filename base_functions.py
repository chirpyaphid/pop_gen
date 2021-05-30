import random

gen_colours = {}

def colour_pheno(genotype):
    if str(genotype) in gen_colours.keys():
        colour = gen_colours[str(genotype)]
        pass
    else:
        colour = (random.randint(60, 245), random.randint(60, 245), random.randint(60, 245))
        gen_colours[str(genotype)] = colour
        pass
    return colour