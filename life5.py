import random
import base_functions as bf
from plants import plant
import pygame

pygame.display.set_caption(f"Sim Window ID: {random.randint(0,10)}")

from window_updates import *
from update_plants_functions import *

males = []
females = []
current_phenos = []
temp = 25
rh = 65

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

        plant.location.x += random.randint(-plant.movement, plant.movement)
        while plant.location.x < base['OUTPUT_WIDTH']:
            plant.location.x += MALE_SPREAD
        while plant.location.x + base['P_WIDTH'] > base['WIDTH']:
            plant.location.x += - MALE_SPREAD

        plant.location.y += random.randint(-plant.movement, plant.movement)
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
                        plant,males,females,temp,rh)

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
                    mplant,
                    males,
                    females,
                temp,
                rh)
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





def main():
    global mode, death,temp,rh
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
                if event.key == pygame.K_DOWN:
                    temp -= 1
                if event.key == pygame.K_UP:
                    temp += 1
                if event.key == pygame.K_LEFT:
                    rh -= 1
                    if rh < 0:
                        rh = 0
                if event.key == pygame.K_RIGHT:
                    rh += 1
                    if rh > 100:
                        rh = 100
                    pass

        if mode == 2:
            male_plants, female_plants, genotypes, current_genotypes = update_plants(males, females)
            draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes,current_phenos,temp,rh)
            if genotypes == 1 or len(male_plants) == 0:
                mode = 3
            try:
                draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes,current_phenos,temp,rh)
            except Exception as e:
                pass

        if mode == 3:
            try:

                draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes,current_phenos,temp,rh)
            except Exception as e:
                rh = 0
                draw_window(male_plants, female_plants, parent_plants, genotypes, current_genotypes,current_phenos,temp,rh)
                print(str(e))
                pass

        if mode == 0:
            draw_window(males, females, parent_plants, 0, [], [],temp,rh)

    pygame.quit()

if __name__ == "__main__":
    main()
