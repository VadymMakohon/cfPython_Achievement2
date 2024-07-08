from django.db import models
from django.shortcuts import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cooking_time = models.PositiveIntegerField()
    description = models.TextField(default="this recipe doesn't have a description yet")
    difficulty = models.CharField(max_length=20, default="N/A")
    ingredients = models.ManyToManyField('ingredients.Ingredient', through='recipesingredients.RecipeIngredient', related_name='recipes')
    pic = models.ImageField(upload_to='recipes', default='no_picture.png') # default stored in src/media

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={'pk': self.pk})