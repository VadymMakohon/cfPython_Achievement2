from django.test import TestCase
from .models import Ingredient

class IngredientModelTest(TestCase):
    def test_create_ingredient(self):
        ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.assertEqual(ingredient.name, "Test Ingredient")