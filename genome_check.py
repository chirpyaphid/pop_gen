
phenotypes2 = {"dom": {
    tuple(['A','A']): "Tall",
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

def check_f_new(new_plant):
    try:
        if tuple(['A','A']) in new_plant.genotype:
            new_plant.location.height = new_plant.location.height * 2

        if tuple(['B','B']) in new_plant.genotype:
            new_plant.location.width = new_plant.location.height * 2

        if tuple(['B','B']) in new_plant.genotype:
            new_plant.life_exp = new_plant.life_exp * 1.5

        if tuple(['b','b']) in new_plant.genotype:
            new_plant.location.width = new_plant.location.height * .5
            new_plant.life_exp = new_plant.life_exp * 2
    except Exception as e:
        pass

    return new_plant

def check_m_new(new_plant):
    try:
        if tuple(['A','A']) in new_plant.genotype:
            new_plant.movement = new_plant.movement * 1.5

        if tuple(['b','b']) in new_plant.genotype:
            new_plant.movement = new_plant.movement * .5
    except Exception as e:
        pass

    return new_plant