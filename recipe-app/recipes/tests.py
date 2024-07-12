from django.test import TestCase
from .models import Recipe
from django.urls import reverse
from ingredients.models import Ingredient
from django.contrib.auth.models import User
from recipes.forms import RecipeSearchForm

class RecipeModelTestCase(TestCase):

    def setUp(self):
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


class RecipeSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some test data for the Recipe and Ingredient models
        ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        recipe1 = Recipe.objects.create(id=1, name="Recipe 1", cooking_time=30)
        recipe2 = Recipe.objects.create(id=2, name="Recipe 2", cooking_time=60)
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)

        # Create additional recipes
        for i in range(3, 13):  # Creates 10 additional recipes with ids 3 to 12
            recipe = Recipe.objects.create(
                id=i, name=f"Recipe {i}", cooking_time=(i + 1) * 10
            )
            recipe.ingredients.add(ingredient1)
            recipe.ingredients.add(ingredient2)

    def setUp(self):
        # Create a test user and log them in for the views requiring login
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_form_fields(self):
        form_data = {
            "Recipe_Name": "Recipe 1",
            "Ingredients": [1],
            "chart_type": "#1",
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_list_view(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_list.html")

    def test_chart_generation(self):
        form_data = {
            "Recipe_Name": "",
            "Ingredients": [1],
            "chart_type": "#1",
        }
        response = self.client.get("/recipes/", form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("chart_image" in response.context)

    def test_view_protected(self):
        self.client.logout()
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/recipes/")

    def test_generate_chart_view(self):
        form_data = {
            "Recipe_Name": "",
            "Ingredients": [1],
            "chart_type": "#1",
        }
        response = self.client.get("/generate-chart/", form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("chart_image" in response.json())