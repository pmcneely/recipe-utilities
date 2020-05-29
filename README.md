### Recipe utilities

This repository contains the raw (publicly available) recipes in my custom take (['inspired'](https://open-recipe-format.readthedocs.io/en/latest/) if you will) on a format on the interwebz. 

Recipes are encoded in a jsonifi-able dictionary as well as dumped into *.yaml and *.json formats, subject to change.  

The `recipe_template.py` objects are meant to provide an API to and from the dictionaries, hand-jammed entries, etc. into the Django model template. Django models may be found at 

For this first pass, ~~recipes are stored in the [Open Recipe Format](https://open-recipe-format.readthedocs.io/en/latest/) where possible.~~ The 'spec' isn't exactly widespread, so I've ~~taken some liberties here and there~~ basically thrown it out but kept useful bits. ~~The recipe format is specified [here](https://open-recipe-format.readthedocs.io/en/latest/topics/reference/orf.html). Nutritional information may eventually be linked using the [associated format](https://open-recipe-format.readthedocs.io/en/latest/topics/reference/onf.html).~~