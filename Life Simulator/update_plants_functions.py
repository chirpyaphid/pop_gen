import random
from gen_settings import *
from genome_check import check_f_new, check_m_new

def new_plant_update(new_plant, alive_m, alive_f, mom, plant,males,females,temp,rh):
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

    # Genome Check
    if new_plant.sex == 'F':
        new_plant = check_f_new(new_plant,temp,rh)
    if new_plant.sex == 'M':
        new_plant = check_m_new(new_plant,temp,rh)

    return new_plant