from django.test import TestCase
from recipes.models import Recipe
from ingredients.models import Ingredient
from recipesingredients.models import RecipeIngredient

# Create your tests here.

class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(name="Test Recipe", cooking_time=30)
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient
        )

    def test_recipe_ingredient_relationship(self):
        self.assertEqual(self.recipe_ingredient.recipe, self.recipe)
        self.assertEqual(self.recipe_ingredient.ingredient, self.ingredient)

    def test_recipe_ingredient_attributes(self):
        self.assertEqual(self.recipe_ingredient.recipe.name, "Test Recipe")
        self.assertEqual(self.recipe_ingredient.ingredient.name, "Test Ingredient")