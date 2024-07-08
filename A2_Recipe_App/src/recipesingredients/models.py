from django.db import models
from recipes.models import Recipe
from ingredients.models import Ingredient

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"


'''
from django.db import models
from recipes.models import Recipe
from ingredients.models import Ingredient
# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipeingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"
'''