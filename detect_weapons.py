from fuzzywuzzy import process

def extract_weapons(text, common_weapons):
    THRESHOLD = 85

    results = process.extract(text, common_weapons)
    weapons = []
    for result in results:
        if result[1] >= THRESHOLD:
            weapons.append(result[0].upper())

    return weapons
