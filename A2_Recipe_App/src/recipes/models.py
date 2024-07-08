from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cooking_time = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=20)
    ingredients = models.ManyToManyField('ingredients.Ingredient', through='recipesingredients.RecipeIngredient', related_name='recipes')

    def __str__(self):
        return self.name


'''
from django.db import models
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cooking_time = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=20)
    ingredients = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.name
    
'''
'''
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('ingredients.Ingredient', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"
'''