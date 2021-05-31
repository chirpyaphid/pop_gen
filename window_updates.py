import collections
import pygame
from gen_settings import *
import terrains as terrains
import base_functions as bf

mode = 1
pygame.init()
gen_colours = bf.gen_colours

WIN = pygame.display.set_mode((base['WIDTH'], base['HEIGHT']))
FONT = pygame.font.SysFont(None, 20)

def draw_window(
        male_plants,
        female_plants,
        parent_plants,
        genotypes,
        current_genotypes,
        current_phenos,
        temp,
        rh=65,
):
    phenos = []
    # print(current_phenos)
    p_types = collections.Counter(phenos)
    try:
        c_phenos = dict(set(current_phenos))
    except Exception as e:
        c_phenos = current_phenos

    WIN.fill(base['BLACK'])
    if len(terrains.terrain_list) == 1:
        pygame.draw.rect(WIN, (0, 0, 0), terrains.DRY_TERRAIN2)
        pygame.draw.rect(WIN, (0, 0, 0), terrains.SWAMP)
        pygame.draw.rect(WIN, (0, 0, 0), terrains.WET_TERRAIN)
    else:
        pygame.draw.rect(WIN, (200, 20, 20), terrains.DRY_TERRAIN)
        # pygame.draw.rect(WIN, (150, 0, 150), terrains.SWAMP)
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

    if base['OUTPUT_WIDTH'] == 0 and mode != 3:
        x = 10
        ambient_text = FONT.render(f"Temp: {temp} / %RH: {rh}", True, base['WHITE'])
        WIN.blit(ambient_text, [5, x])
        x += 25

        m_count = FONT.render(f"Males TD: {bf.total_males}", True, base['WHITE'])
        WIN.blit(m_count, [5, x])
        x += 25
        f_count = FONT.render(f"Females TD: {bf.total_females}", True, base['WHITE'])
        WIN.blit(f_count, [5, x])
        x += 25
        p_count = FONT.render(f"Phenos: {len(c_phenos)}", True, base['YELLOW'])
        WIN.blit(p_count, [5, x])
        x += 15
        g_count = FONT.render(f"Genotypes: {genotypes}", True, base['WHITE'])
        WIN.blit(g_count, [5, x])

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
