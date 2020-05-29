import ruamel.yaml
import uuid


class RecipeYAML:
    def __init__(self, name, description=None):
        self.oven_fan = None
        self.oven_temp = None
        self.oven_time = None
        self.notes = ""
        self.recipe_name = name
        self.description = description
        self.recipe_uuid = str(uuid.uuid1())
        self.source_book = None
        self.source_authors = None
        self.source_url = None
        self.components = []  # List of Components
        self.stages = []  # List of Stages
        self.yields = []  # List of Yields

    def add_component(self, Component):
        self.components.append(Component.to_dict())

    def add_stage(self, Stage):
        self.stages.append(Stage.to_dict())

    def add_yield(self, Yield):
        self.yields.append(Yield.to_dict())

    def add_note(self, note):
        self.notes.append(note)

    def to_dict(self):
        d = {}
        for field, value in self.__dict__.items():
            if value:
                d[field] = value
        return d


class StageYAML:
    def __init__(self, name):
        self.name = name  # Another break from 'official' spec
        self.steps = []
        self.haccp = None  # Either 'control_point' or 'critical_control_point'
        self.notes = []

    def add_step(self, Step):
        self.steps.append(Step.to_dict())

    def add_note(self, note):
        self.notes.append(note)

    def to_dict(self):
        return {
            "name": self.name,
            "steps": self.steps,
            "haccp": self.haccp,
            "notes": self.notes,
        }


class StepYAML:
    def __init__(self, instruction):
        self.instruction = None
        self.notes = None
        if type(instruction) is str:
            self.instruction = instruction
        elif type(instruction) is dict:
            assert not set(instruction.keys()).difference(
                {"ins", "notes"}
            ), "Only instructions and notes or strings are allowed for instructions"
            self.instruction = instruction["ins"]
            self.notes = instruction["notes"]

    def to_dict(self):
        if self.notes:
            return {"instruction": self.instruction, "notes": self.notes}
        else:
            return {"instruction": self.instruction}


class ComponentYAML:
    def __init__(self, name):
        self.name = name
        self.ingredients = []  # List of Ingredients

    def add_ingredient(self, Ingredient):
        self.ingredients.append(Ingredient.to_dict())

    def to_dict(self):
        return {'name': self.name, 'ingredients': self.ingredients}

class IngredientYAML:
    def __init__(self, name):
        self.name = name
        self.amount = 0
        self.unit = ""
        self.notes = ""
        self.substitutions = []  # A list of Ingredients objects in substitution
        # list of tags, e.g. “whole”, “large dice”, “minced”, “raw”, “steamed”, etc.
        self.processing = []
        self.usda_num = 0

    def to_dict(self):

        return {
            "name": self.name,
            "amount": self.amount,
            "processing": self.processing,
            "notes": self.notes,
            "substitutions": [sub.to_dict() for sub in self.substitutions],
            "usda_num": self.usda_num,
        }


class YieldYAML:
    def __init__(self, amount, unit):

        self.amount = amount
        self.unit = unit

    def to_dict(self):
        return {"amount": self.amount, "unit": self.unit}


class OvenTempYAML:
    def __init__(self):

        self.amount = None
        self.unit = None

    def to_dict(self):
        return {"amount": self.amount, "unit": self.unit}


class CookBookYAML:
    def __init__(self):
        self.authors = []  # list of authors
        self.title = ""
        self.isbn = 0
        self.notes = ""
        self.x_fields = None

    def to_dict(self):
        return {
            "authors": self.authors,
            "title": self.title,
            "isbn": self.isbn,
            "notes": self.notes,
            "other": self.x_fields,
        }
