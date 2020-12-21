from helpers import *

test_data = Data("""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""")

test_case(1, test_data, 5)
test_case(2, test_data, "mxmxvkd,sqjhc,fvjkl")


def part1_and_2(d: Data, ans: Answers) -> None:
    non_allergenic_ingredient_count = Counter()
    allergens_to_possible_ingredients = defaultdict(IntersectionSet)

    for ingredients, allergens in d.parsed_lines('<> (contains <>)'):
        ingredients = ingredients.split()
        non_allergenic_ingredient_count.update(ingredients)

        for allergen in allergens.stripsplit(','):
            allergens_to_possible_ingredients[allergen].intersection_update(
                ingredients
            )

    ingredient_to_allergen = {}
    while allergens_to_possible_ingredients:
        found_allergen = min(
            allergens_to_possible_ingredients,
            key=lambda i: len(allergens_to_possible_ingredients[i])
        )
        allergenic_ingredient = scalar(
            allergens_to_possible_ingredients.pop(found_allergen)
        )

        non_allergenic_ingredient_count.pop(allergenic_ingredient)
        ingredient_to_allergen[allergenic_ingredient] = found_allergen
        for allergen in allergens_to_possible_ingredients:
            (allergens_to_possible_ingredients[allergen]
             .discard(allergenic_ingredient))

    ans.part1 = sum(non_allergenic_ingredient_count.values())
    ans.part2 = ','.join(
        sorted(
            ingredient_to_allergen,
            key=lambda x: ingredient_to_allergen[x]
        )
    )


run([1, 2], day=21, year=2020)
