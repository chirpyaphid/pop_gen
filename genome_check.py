phenotypes2 = {"dom": {
    tuple(['A', 'A']): "Tall",
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


def check_f_new(new_plant, temp, rh):
    # return new_plant
    try:
        if ('b', 'b') in new_plant.genotype and ('A', 'A') in new_plant.genotype:
            pass
            new_plant.location.height = new_plant.location.height * 4
            new_plant.location.width = new_plant.location.width * .25
            # new_plant.max_pollination_count = 100

            # if temp >= 25 <= 28:
            #     new_plant.life_exp = new_plant.life_exp * 1.5
            # elif temp > 28 <= 33:
            #     new_plant.life_exp = new_plant.life_exp * 1.2
            # elif temp > 33:
            #     new_plant.life_exp = new_plant.life_exp * .9
            # elif temp < 23:
            #     new_plant.life_exp = new_plant.life_exp * .9
            # elif temp < 10:
            #     new_plant.life_exp = new_plant.life_exp * 0
        else:
            if ('A', 'A') in new_plant.genotype:
                new_plant.location.height = new_plant.location.height * 3
                new_plant.life_exp = new_plant.life_exp * 1.08
                # if temp >= 25 <= 30:
                #     new_plant.life_exp = new_plant.life_exp * 1.2
                # elif temp > 30:
                #     new_plant.life_exp = new_plant.life_exp * .9
                # elif temp > 35:
                #     new_plant.life_exp = new_plant.life_exp * .5
                # elif temp < 22:
                #     new_plant.life_exp = new_plant.life_exp * .4
                # elif temp < 10:
                #     new_plant.life_exp = new_plant.life_exp * 0

            if ('a', 'a') in new_plant.genotype:
                pass
                new_plant.location.height = new_plant.location.height * .25
                # if temp >= 22 <= 27:
                #     new_plant.life_exp = new_plant.life_exp * 1.2
                # elif temp > 27:
                #     new_plant.life_exp = new_plant.life_exp * .6
                # elif temp > 35:
                #     new_plant.life_exp = new_plant.life_exp * 0
                # elif temp < 22:
                #     new_plant.life_exp = new_plant.life_exp * .8
                # elif temp < 10:
                #     new_plant.life_exp = new_plant.life_exp * .5

            if ('B', 'B') in new_plant.genotype:
                new_plant.location.width = new_plant.location.width * 1.5
                # new_plant.life_exp = new_plant.life_exp * .5
                # if temp >= 22 <= 27:
                #     new_plant.life_exp = new_plant.life_exp * 1.2
                # elif temp > 27:
                #     new_plant.life_exp = new_plant.life_exp * .6
                # elif temp > 35:
                #     new_plant.life_exp = new_plant.life_exp * 0
                # elif temp < 22:
                #     new_plant.life_exp = new_plant.life_exp * .8
                # elif temp < 10:
                #     new_plant.life_exp = new_plant.life_exp * .5

            if ('b', 'b') in new_plant.genotype:
                new_plant.location.width = new_plant.location.width * .5
                new_plant.life_exp = new_plant.life_exp * 1.09
                # if temp >= 25 <= 30:
                #     new_plant.life_exp = new_plant.life_exp * 1.2
                # elif temp > 30:
                #     new_plant.life_exp = new_plant.life_exp * .9
                # elif temp > 35:
                #     new_plant.life_exp = new_plant.life_exp * .5
                # elif temp < 22:
                #     new_plant.life_exp = new_plant.life_exp * .4
                # elif temp < 10:
                #     new_plant.life_exp = new_plant.life_exp * 0

            if ('C', 'c') in new_plant.genotype:
                new_plant.life_exp = new_plant.life_exp * 1.01
    except Exception as e:
        pass

    return new_plant


def check_m_new(new_plant, temp, rh):
    return new_plant
    try:
        if ('A', 'A') in new_plant.genotype:
            new_plant.movement = new_plant.movement * 1.5

        if ('b', 'b') in new_plant.genotype:
            new_plant.movement = new_plant.movement * .5
        if ('b', 'b') in new_plant.genotype and ('A', 'A') in new_plant.genotype:
            if temp >= 25 <= 30:
                new_plant.life_exp = new_plant.life_exp * 2
            elif temp > 30:
                new_plant.life_exp = new_plant.life_exp * 10
            elif temp > 35:
                new_plant.life_exp = new_plant.life_exp * .9
            elif temp < 22:
                new_plant.life_exp = new_plant.life_exp * .2
            elif temp < 10:
                new_plant.life_exp = new_plant.life_exp * 0
        else:
            if ('A', 'A') in new_plant.genotype:
                if temp >= 25 <= 30:
                    new_plant.life_exp = new_plant.life_exp * 1.2
                elif temp > 30:
                    new_plant.life_exp = new_plant.life_exp * .9
                elif temp > 35:
                    new_plant.life_exp = new_plant.life_exp * .5
                elif temp < 22:
                    new_plant.life_exp = new_plant.life_exp * .4
                elif temp < 10:
                    new_plant.life_exp = new_plant.life_exp * 0

            if ('a', 'a') in new_plant.genotype:
                if temp >= 22 <= 27:
                    new_plant.life_exp = new_plant.life_exp * 1.2
                elif temp > 27:
                    new_plant.life_exp = new_plant.life_exp * .6
                elif temp > 35:
                    new_plant.life_exp = new_plant.life_exp * 0
                elif temp < 22:
                    new_plant.life_exp = new_plant.life_exp * .8
                elif temp < 10:
                    new_plant.life_exp = new_plant.life_exp * .5

            if ('B', 'B') in new_plant.genotype:
                if temp >= 22 <= 27:
                    new_plant.life_exp = new_plant.life_exp * 1.2
                elif temp > 27:
                    new_plant.life_exp = new_plant.life_exp * .6
                elif temp > 35:
                    new_plant.life_exp = new_plant.life_exp * 0
                elif temp < 22:
                    new_plant.life_exp = new_plant.life_exp * .8
                elif temp < 10:
                    new_plant.life_exp = new_plant.life_exp * .5

            if ('b', 'b') in new_plant.genotype:
                if temp >= 25 <= 30:
                    new_plant.life_exp = new_plant.life_exp * 1.2
                elif temp > 30:
                    new_plant.life_exp = new_plant.life_exp * .9
                elif temp > 35:
                    new_plant.life_exp = new_plant.life_exp * .5
                elif temp < 22:
                    new_plant.life_exp = new_plant.life_exp * .4
                elif temp < 10:
                    new_plant.life_exp = new_plant.life_exp * 0

            if ('C', 'c') in new_plant.genotype:
                new_plant.life_exp = new_plant.life_exp * 1.5

    except Exception as e:
        pass

    return new_plant
