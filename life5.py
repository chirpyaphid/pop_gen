import random
import pygame
# import os
import base_functions as bf
from gen_settings import *
from plants import plant
import terrains as terrains
import collections

pygame.init()

gen_colours = bf.gen_colours

WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 20)

mode = 1

males = []
females = []
current_phenos = []

p1 = [('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'd')]#, ('E', 'e'), ('F', 'f')]
p2 = [('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'd')]#, ('E', 'e')]#, ('F', 'f')]

parents = [p1, p2]

phenotypes = {"dom": {
    "A": "Tall",
    "B": "Broad Leaf",
    "C": "Citrus",
    "D": "Green",
    "E": "Pine",
    "F": "THC"
},
    "res": {
        "a": "Short",
        "b": "Narrow Leaf",
        "c": "Earthy",
        "d": "Purple",
        "e": "Fuel",
        "f": "CBD"
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


def draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes):
    phenos = []

    WIN.fill(base['BLACK'])
    if len(terrains.terrain_list) == 1:
        pygame.draw.rect(WIN, (0, 0, 0), terrains.DRY_TERRAIN2)
        pygame.draw.rect(WIN, (0, 0, 0), terrains.SWAMP)
        pygame.draw.rect(WIN, (0, 0, 0), terrains.WET_TERRAIN)
    else:
        pygame.draw.rect(WIN, (200, 20, 20), terrains.DRY_TERRAIN)
        pygame.draw.rect(WIN, (150, 0, 150), terrains.SWAMP)
        pygame.draw.rect(WIN, (20, 20, 200), terrains.WET_TERRAIN)

    for plant in male_plants:
        pheno, color = plant.pheno()

        if tuple([tuple(pheno), color]) not in current_phenos:
            current_phenos.append(tuple([tuple(pheno), color]))
        else:
            pass
        phenos.append(tuple(pheno))
        if plant.state == 'Alive':
            cell, colour = plant.cell()
            pygame.draw.rect(WIN, base['YELLOW'], cell)
            pygame.draw.rect(WIN, gen_colours[str(plant.genotype)], cell)

    for plant in female_plants:
        pheno, c = plant.pheno()
        pheno = tuple(pheno)
        phenos.append(pheno)
        if plant.state == 'Alive':
            cell, colour = plant.cell()
            pygame.draw.rect(WIN, colour, cell)
    if base['OUTPUT_WIDTH'] != 0:
        x = 25

        p1 = FONT.render(f"P1 Pheno {parent_plants[0].pheno()[0]}", True, gen_colours[str(parent_plants[0].genotype)])
        p1g = FONT.render(f"P1 Geno {parent_plants[0].genotype}", True, gen_colours[str(parent_plants[0].genotype)])
        WIN.blit(p1, [5, x])
        x += 15
        WIN.blit(p1g, [5, x])
        x += 15

        p2 = FONT.render(f"P2 Pheno {parent_plants[1].pheno()[0]}", True, gen_colours[str(parent_plants[1].genotype)])
        p2g = FONT.render(f"P2 Pheno {parent_plants[1].genotype}", True, gen_colours[str(parent_plants[1].genotype)])
        WIN.blit(p2, [5, x])
        x += 15
        WIN.blit(p2g, [5, x])
        x += 15

        m_count = FONT.render(f"Males: {len(male_plants)}", True, base['WHITE'])
        WIN.blit(m_count, [5, x])
        x += 20
        m_count = FONT.render(f"Males TD: {bf.total_males}", True, base['WHITE'])
        WIN.blit(m_count, [5, x])
        x += 25

        f_count = FONT.render(f"Females: {len(female_plants)}", True, base['WHITE'])
        WIN.blit(f_count, [5, x])
        x += 20
        f_count = FONT.render(f"Females TD: {bf.total_females}", True, base['WHITE'])
        WIN.blit(f_count, [5, x])
        x += 25

        p_types = collections.Counter(phenos)

        g_count = FONT.render(f"Genotypes: {genotypes}", True, base['WHITE'])
        WIN.blit(g_count, [5, x])
        x += 30

        max_gen_text = FONT.render(f"Max Gen: {max_gen}", True, base['YELLOW'])
        WIN.blit(max_gen_text, [5, x])
        # x += 20
        # max_mage_text = FONT.render(f"Max Mom Age: {max_mom_age}", True, base['YELLOW'])
        # WIN.blit(max_mage_text, [5, x])
        x += 25

        p_count = FONT.render(f"Phenos: {len(set(p_types))}", True, base['YELLOW'])
        WIN.blit(p_count, [5, x])
        x += 15
        p_types = collections.Counter(phenos)
        c_phenos = dict(set(current_phenos))

        for p in p_types:
            try:
                p_count = FONT.render(f"Pheno: {p} Count: {p_types[p]}", True, c_phenos[p])
                WIN.blit(p_count, [5, x])
                x += 15

            except Exception as e:
                pass
    # print(gen_colours)
    if mode == 3:
        pygame.draw.rect(WIN, (0, 0, 0), END_BACK)
        if base['OUTPUT_WIDTH'] == 0:
            x = 0
        x += 10
        t_males = FONT.render(f"Total Males: {bf.total_males} ", True, base['YELLOW'])
        WIN.blit(t_males, [5, x])
        x += 15
        t_males = FONT.render(f"Total Females: {bf.total_females} ", True, base['YELLOW'])
        WIN.blit(t_males, [5, x])
        x += 15

        p1 = FONT.render(f"P1 Pheno {parent_plants[0].pheno()[0]}", True, gen_colours[str(parent_plants[0].genotype)])
        p1g = FONT.render(f"P1 Geno {parent_plants[0].genotype}", True, gen_colours[str(parent_plants[0].genotype)])
        WIN.blit(p1, [5, x])
        x += 15
        WIN.blit(p1g, [5, x])
        x += 15

        p2 = FONT.render(f"P2 Pheno {parent_plants[1].pheno()[0]}", True, gen_colours[str(parent_plants[1].genotype)])
        p2g = FONT.render(f"P2 Pheno {parent_plants[1].genotype}", True, gen_colours[str(parent_plants[1].genotype)])
        WIN.blit(p2, [5, x])
        x += 15
        WIN.blit(p2g, [5, x])
        x += 20

        max_gen_text = FONT.render(f"Max Gen: {max_gen}", True, base['YELLOW'])
        WIN.blit(max_gen_text, [5, x])
        x += 15
        max_mutations_text = FONT.render(f"Max Mutations: {mutation_count}", True, base['YELLOW'])
        WIN.blit(max_mutations_text, [5, x])
        x += 20
        for g in current_genotypes:
            g_type = FONT.render(f"Genotype: {g} ", True, gen_colours[str(g)])
            WIN.blit(g_type, [5, x])
            x += 15

    pygame.display.update()


def a_colour_pheno(genotype):
    if str(genotype) in gen_colours.keys():
        colour = gen_colours[str(genotype)]
        pass
    else:
        colour = (random.randint(60, 245), random.randint(60, 245), random.randint(60, 245))
        gen_colours[str(genotype)] = colour
        pass
    return colour


def update_plants(in_males, in_females):
    global death, males, females
    alive_m = []
    alive_f = []

    for p in in_males:
        if p.state == 'Alive':
            if len(alive_f) + len(alive_m) > MAX_POP * 1.1:
                p.life_exp = p.life_exp * .05
            for terrain in terrains.terrain_list:
                if p.location.colliderect(terrain['terrain']):
                    terrains.run_check(p, phenotypes, terrain['type'])
                p.age += 1
                alive_m.append(p)

    for p in in_females:
        if p.state == 'Alive':
            if len(alive_f) + len(alive_m) > MAX_POP * 1.1:
                p.life_exp = p.life_exp * .05
            for terrain in terrains.terrain_list:
                if p.location.colliderect(terrain['terrain']):
                    terrains.run_check(p, phenotypes, terrain['type'])
                p.age += 1
            alive_f.append(p)

    for mom in alive_f:
        if mom.age > plant_details['mm_age']:
            max_mom_age[0] = 0
            if len(alive_f) + len(alive_m) > MAX_POP * 1.5:
                mom.state = 'Dead'
            else:
                if len(alive_f) > MAX_POP * event_triggers['pop_trigger1']:
                    offspring = 2
                elif len(alive_f) < MAX_POP * event_triggers['pop_trigger2']:
                    offspring = 20
                else:
                    offspring = 50

                for x in range(0, offspring):
                    pollination = 's'
                    new_plant = bf.create_crosses(mom, mom, len(alive_f), len(alive_m), 's', phenotypes)
                    new_plant.sex = 'F'
                    new_plant_update(new_plant,
                                     len(alive_m),
                                     len(alive_f),
                                     mom,
                                     mom)
                    for terrain in terrains.terrain_list:
                        if new_plant.location.colliderect(terrain['terrain']):
                            terrains.run_check(new_plant, phenotypes, terrain['type'])

                mom.pollination_count += 1
                if mom.pollination_count >= mom.max_pollination_count:
                    mom.state = 'Dead'

    for plant in alive_m:
        if len(alive_m) < plant_details['min_males']:
            pass
        else:
            if plant.life_exp > 1:
                plant.life_exp -= 1
            else:
                plant.life_exp = 0
                plant.state = 'Dead'

        plant.location.x += random.randint(plant_details['male_movement_min'], plant_details['male_movement'])
        while plant.location.x < base['OUTPUT_WIDTH']:
            plant.location.x += MALE_SPREAD
        while plant.location.x + base['P_WIDTH'] > base['WIDTH']:
            plant.location.x += - MALE_SPREAD

        plant.location.y += random.randint(plant_details['male_movement_min'], plant_details['male_movement'])
        while plant.location.y < 0:
            plant.location.y += MALE_SPREAD
        while plant.location.y + base['P_HEIGHT'] > base['HEIGHT']:
            plant.location.y += -MALE_SPREAD

        for mom in alive_f:

            if len(alive_f) <= 5:
                pass
            else:
                if mom.life_exp > 1:
                    mom.life_exp -= 1
                else:
                    mom.life_exp = 0
                    mom.state = 'Dead'

            if plant.location.colliderect(mom.location) and mom.state == 'Alive' and plant.state == 'Alive':
                if len(alive_f) + len(alive_m) > MAX_POP:
                    offspring = 1
                elif len(alive_f) + len(alive_m) >= MAX_POP * event_triggers['pop_trigger1']:
                    offspring = 2
                elif len(alive_f) + len(alive_m) < MAX_POP * event_triggers['pop_trigger1']:
                    offspring = 3
                elif len(alive_f) + len(alive_m) < MAX_POP * event_triggers['pop_trigger2']:
                    offspring = 4
                elif len(alive_f) + len(alive_m) < MAX_POP * event_triggers['pop_trigger3']:
                    offspring = 7

                for x in range(0, offspring):
                    new_plant = new_plant_update(
                        bf.create_crosses(mom, plant, len(alive_f), len(alive_m), 'x', phenotypes),
                        len(alive_m),
                        len(alive_f),
                        mom,
                        plant)

                plant.state = 'Dead'
                mom.pollination_count += 1
                if mom.pollination_count > mom.max_pollination_count:
                    mom.state = 'Dead'
                # print(mom.offspring,mom.state)

    if len(alive_m) < plant_details['min_males']:
        try:
            mplant = alive_m[random.randint(0, len(alive_m))]
            offspring = 4
            for x in range(0, offspring):
                new_plant = new_plant_update(
                    bf.create_crosses(mplant, mplant, len(alive_f), len(alive_m), 'x', phenotypes),
                    len(alive_m),
                    len(alive_f),
                    mplant,
                    mplant)
            mplant.state = 'Dead'
        except Exception as e:
            pass

    alive_m = []
    alive_f = []
    genotypes = []
    for p in males:
        if p.state == 'Alive':
            alive_m.append(p)
            if p.genotype not in genotypes:
                genotypes.append(p.genotype)
    for p in females:
        if p.state == 'Alive':
            alive_f.append(p)
            if p.age > max_mom_age[0]:
                max_mom_age[0] = p.age
            if p.genotype not in genotypes:
                genotypes.append(p.genotype)
    males = alive_m
    females = alive_f
    return alive_m, alive_f, len(genotypes), genotypes


def new_plant_update(new_plant, alive_m, alive_f, mom, plant):
    if new_plant.sex == 'F':
        new_plant.life_exp = new_plant.life_exp + random.randint(plant_details['f_life_min'],
                                                                 plant_details['f_life_max'])
        new_plant.location.x = mom.location.x + random.randint(plant_details['female_spread_min'],
                                                               plant_details['female_spread'])
        while new_plant.location.x > base['WIDTH'] + base['P_WIDTH']:
            new_plant.location.x = mom.location.x + random.randint(-200, -100)
        while new_plant.location.x < 0:
            new_plant.location.x = mom.location.x + random.randint(100, 200)

        new_plant.location.y = mom.location.y + random.randint(plant_details['female_spread_min'],
                                                               plant_details['female_spread'])
        while new_plant.location.y > base['HEIGHT'] + base['P_HEIGHT']:
            new_plant.location.y = mom.location.y + random.randint(-200, -100)
        while new_plant.location.y < 0:
            new_plant.location.y = mom.location.y + random.randint(100, 200)
        females.append(new_plant)
    else:
        new_plant.location.x = plant.location.x + random.randint(plant_details['male_spread_min'],
                                                                 plant_details['male_spread'])
        new_plant.location.y = plant.location.y + random.randint(plant_details['male_spread_min'],
                                                                 plant_details['male_spread'])
        males.append(new_plant)

    if new_plant.sex == 'F':
        for gt in new_plant.genotype:
            check = gt[0] + gt[1]
            if check in phenotypes['codom'].keys():

                for codom in phenotypes['codom'].keys():

                    if check == codom:

                        for attrib in phenotypes['codom'][codom].keys():
                            if attrib == 'size':
                                new_plant.location.height = new_plant.location.height * \
                                                            phenotypes['codom'][codom][
                                                                attrib]
                                new_plant.location.width = new_plant.location.width * phenotypes['codom'][codom][
                                    attrib]
                            elif attrib == 'height':
                                new_plant.location.height = new_plant.location.height * \
                                                            phenotypes['codom'][codom][
                                                                attrib]
                            elif attrib == 'width':
                                new_plant.location.width = new_plant.location.width * phenotypes['codom'][codom][
                                    attrib]
                            elif attrib == 'life_exp':
                                new_plant.life_exp = new_plant.life_exp * phenotypes['codom'][codom][attrib]
            if check in phenotypes['linked'].keys():
                for linked in phenotypes['linked'].keys():
                    if check == linked:
                        for attrib in phenotypes['linked'][linked].keys():
                            if attrib == 'size':
                                new_plant.location.height = new_plant.location.height * phenotypes['linked'][linked][
                                    attrib]
                                new_plant.location.width = new_plant.location.width * phenotypes['linked'][linked][
                                    attrib]
                            elif attrib == 'height':
                                new_plant.location.height = new_plant.location.height * phenotypes['linked'][linked][
                                    attrib]
                            elif attrib == 'width':
                                new_plant.location.width = new_plant.location.width * phenotypes['linked'][linked][
                                    attrib]
                            elif attrib == 'life_exp':
                                new_plant.life_exp = new_plant.life_exp * phenotypes['linked'][linked][attrib]

    return new_plant


def main():
    global mode, death
    parent_plants = []
    plants = []
    start = 1
    for p in parents:
        parent = plant(p, 'Test', phenotypes, 3)
        parent_plants.append(parent)
    while mode == 1:
        for x in range(0, base['start_pop']):
            new_plant = bf.create_crosses(parent_plants[0], parent_plants[1], x, x, 'x', phenotypes)
            if new_plant.sex == 'F':
                females.append(new_plant)
            else:
                males.append(new_plant)
            plants.append(new_plant)
        male_plants = males
        female_plants = females
        mode = 0
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(base['FPS'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    mode = 2
                if event.key == pygame.K_RCTRL:
                    mode = 0
                if event.key == pygame.K_1:
                    death = 10
                    pass
        if mode == 2:
            male_plants, female_plants, genotypes, current_genotypes = update_plants(males, females)
            draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes)
            if genotypes == 1 or len(male_plants) == 0:
                mode = 3
            try:
                draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes)
                # if genotypes == 1 or len(male_plants) == 0:
                #     mode = 3
            except Exception as e:
                pass
        if mode == 3:
            draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes)
        if mode == 0:
            draw_window(males, females, parent_plants, 0, [])

    pygame.quit()


if __name__ == "__main__":
    main()
