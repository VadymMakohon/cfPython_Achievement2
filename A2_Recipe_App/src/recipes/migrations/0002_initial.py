# Generated by Django 5.0.6 on 2024-07-08 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0001_initial'),
        ('recipesingredients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipesingredients.RecipeIngredient', to='ingredients.ingredient'),
        ),
    ]
