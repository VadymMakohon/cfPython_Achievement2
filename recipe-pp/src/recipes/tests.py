from django.test import TestCase
from .models import Recipe
from ingredients.models import Ingredient

# Create your tests here.
class RecipeModelTestCase(TestCase):

    def setUp(self):
        # Set up test data
        self.ingredient = Ingredient.objects.create(name='Test Ingredient')
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            cooking_time=5,
            difficulty='Easy'
        )
        self.recipe.ingredients.add(self.ingredient)

    def test_recipe_has_ingredient(self):
        self.assertEqual(self.recipe.ingredients.count(), 1)
        self.assertEqual(self.recipe.ingredients.first(), self.ingredient)

    def test_get_absolute_url(self):
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            cooking_time=5,
            difficulty='Easy'
        )
        self.assertEqual(self.recipe.get_absolute_url(), "/list/2")