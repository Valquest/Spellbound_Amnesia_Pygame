from variables import constants

def modify(to_modify):
    print(to_modify)
    for card_index in to_modify:
        print("works")

if 5 == constants.CARD_COUNT:
    modify([constants.CARD_COUNT])