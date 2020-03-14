import json
import utils
import random


class RecipeDB:
    # initialize the recipeDB.json file
    def __init__(self, path):
        # open the file
        with open(path) as f:
            # load the data
            json_data = json.load(f)
            # process all of the content in the database
            # for example, set self.tools to be an array of tools 
            self.tools = json_data["tools"]

            # set of descriptions
            self.meat = json_data["descriptions"]["meat"]
            self.seafood = json_data["descriptions"]["seafood"]
            self.dessert = json_data["descriptions"]["dessert"]
            self.veggie = json_data["descriptions"]["veggie"]
            self.other = json_data["descriptions"]["veggie"]

            # set of preparation
            self.hardFoodPrep = json_data["preparation"]["hardFoodPrep"]
            self.regularFoodPrep = json_data["preparation"]["regularFoodPrep"]

            # set of seasons
            self.seasonings = json_data["seasonings"]

            # set of styles
            self.styles = json_data["styles"]

            # set of measurements
            self.solidMeasurements = json_data["measurement"]["solids"]
            self.liquidMeasurements = json_data["measurement"]["liquids"]

            # set of cooking methods
            self.primaryMethods = json_data["methods"]["primary"]
            self.secondaryMethods = json_data["methods"]["secondary"]

            # parse and get the healthy to unhealthy transformations
            # get the structure
            healthyAndUnhealthy = json_data["healthyToUnhealthy"]
            self.healthyToUnhealthy = {
                pairs["healthy"]: pairs["unhealthy"]
                for pairs in healthyAndUnhealthy
            }
            self.unhealthyToHealthy = {
                pairs["unhealthy"]: pairs["healthy"]
                for pairs in healthyAndUnhealthy
            }
            self.chinese = json_data["to_chinese"]
            self.indian = json_data["to_indian"]

    # function that determines if there is something present in some collection
    # this is run for all of the methods so I am making a function
    def _presentInCollection(self, item, collection):
        # for all of the elements in the collection
        for i in collection:
            if (i in item):
                return True
            else:
                # item was not in collection
                return False

    # checking if some ingredient is present in a collection 
    def _isIngredientType(self, ingredient, collection):
        return self._presentInCollection(ingredient.name, collection)

    def _isMeatPresent(self, ingredient):
        meatIsPresent = self._isIngredientType(ingredient, self.meat)
        return meatIsPresent

    # checks to see if an ingredient is healthy
    def _isUnhealthy(self, ingredient):
        # keys() returns all of the dictionary keys as a list
        return self._isIngredientType(ingredient, self.unhealthyToHealthy.keys())

    # checks to see if an ingredient is unhealthy
    def _isHealthy(self, ingredient):
        return self._isIngredientType(ingredient, self.healthyToUnhealthy.keys())

    
