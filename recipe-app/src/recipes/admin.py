from django.contrib import admin
from django.contrib import admin
from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'difficulty', 'display_ingredients','description')

    def display_ingredients(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])
    display_ingredients.short_description = 'Ingredients'

# Register your models here.
admin.site.register(Recipe, RecipeAdmin)