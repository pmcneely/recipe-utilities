#!/usr/bin/env python3

import json
import os
import sys

from ruamel.yaml import YAML

import recipe_template as rt

def get_basic_recipe():

    recipe = {
        "title": "Generified recipe",
        "description": "A basic recipe template, loosely adapted. I highly doubt this would taste good - don't make it!",
        "dish_image": "foodie_image.png",
        "components": {
            "Main": {
                "noodles": {"qty": 8, "units": "oz"},
                "oil": {"qty": 3, "units": "tbsp"},
                "garlic": {"qty": 3, "units": "cloves", "instructions": "minced"},
                "eggs": {"qty": 2, "units": "", "instructions": "lightly beaten/mixed"},
                "chicken": {
                    "qty": 8,
                    "units": "oz",
                    "instructions": "Cut bite-size",
                },
                "sweet capsicum, green": {
                    "qty": 1,
                    "units": "",
                    "instructions": "thinly sliced",
                },
                "green onions": {"qty": 3, "units": "", "instructions": "chopped"},
                "onion": {"qty": 0.5, "units": "cup", "instructions": "julienned/thinly sliced"}
            },
            "tasty sauce": {
                "fish sauce": {"qty": 3, "units": "tbsp"},
                "soy sauce": {"qty": 1, "units": "tbsp"},
                "palm sugar": {"qty": 5, "units": "tbsp"},
                "tamarind paste": {
                    "qty": 2,
                    "units": "tbsp",
                    "substitutions": {"rice vinegar": {"qty": 2, "units": "tbsp"},},
                },
            },
        },
        "stages": {
            "Noodles": [
                "Cook noodles according to package instructions.",
            ],
            "Sauce": ["Mix the sauce ingredients together. Set aside while preparing the rest of the ingredients",],
            "Main": [
                "Heat oil in a large saucepan, allow to reach even heat at medium/medium-high.",
                "Add the onion, garlic and capsicum. Sautee until wilted, about 3-5 minutes.",
                "Add chicken, cook until just cooked through, about 3-4 more minutes.",
                "Add a little more oil and add the beaten eggs. Scramble the eggs while cooking.",
                "Add noodles, sauce. Toss everything to combine.",
            ],
        },
        "url": "https://172.10.0.2/this-address-is-not-dns-addressable/",
        "book": "my upcoming book, ca. 2095",
        "text_link": "",
    }

    return recipe


def get_ingredient(ingredient, description):

    i = rt.IngredientYAML(ingredient)
    i.amount = description.get("qty")
    i.unit = description.get("units")
    i.notes = description.get("notes")
    i.processing = description.get("processing", None)

    return i

def usage():

    print("Usage: ./build_base_recipe.py ."
    "Namespace issues will probably break the script otherwise")
    sys.exit()

if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.realpath(__file__))

    d = get_basic_recipe()

    recipe = rt.RecipeYAML(d["title"], description=d["description"])
    recipe.source_url = d["url"]

    for component, ingredients in d["components"].items():
        c = rt.ComponentYAML(component)
        for ingredient, description in ingredients.items():
            i = get_ingredient(ingredient, description)
            subs = description.get("substitutions", None)
            if subs is not None:
                for name, ins in subs.items():
                    assert (
                        "substitutions" not in ins.keys()
                    ), "Substitutions of substitutions is only peering into the void"
                    i.substitutions.append(get_ingredient(name, ins))
            c.add_ingredient(i)
        recipe.add_component(c)

    for stage, instructions in d["stages"].items():
        s = rt.StageYAML(stage)
        for ins in instructions:
            s.add_step(rt.StepYAML(ins))
        recipe.add_stage(s)

    yaml = YAML()

    readable_path = os.path.join(script_dir, "recipes/expanded_readable.yaml")
    readable_compact_path = os.path.join(script_dir, "recipes/readable_compact.json")
    compact_path = os.path.join(script_dir, "recipes/compact.json")

    with open(readable_path, "w") as recipe_output:
        yaml.dump(recipe.to_dict(), recipe_output)
    recipe_output.close()

    with open(readable_compact_path, "w") as recipe_output:
        recipe_output.write(json.dumps(recipe.to_dict(), indent=2))
    recipe_output.close()

    with open(compact_path, "w") as recipe_output:
        recipe_output.write(json.dumps(recipe.to_dict()))
    recipe_output.close()

else:
    usage()