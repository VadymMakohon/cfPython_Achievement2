from io import BytesIO
import base64
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from typing import Any, Dict
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.db import transaction

from .models import Recipe
from recipesingredients.models import RecipeIngredient
from .forms import RecipeSearchForm, RecipeForm, NewIngredientForm
from ingredients.models import Ingredient


# Create your views here.
def recipes_home(request):
    return render(request, "recipes/recipes_home.html")

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)

    if chart_type == "#1":
        # Bar Chart
        plt.title("Cooking Time by Recipe", fontsize=20)
        plt.bar(data["name"], data["cooking_time"])
        plt.xlabel("Recipes", fontsize=16)
        plt.ylabel("Cooking Time (min)", fontsize=16)
    elif chart_type == "#2":
        # Pie Chart
        plt.title("Recipes Cooking Time Comparison", fontsize=20)
        labels = kwargs.get("labels")
        plt.pie(data["cooking_time"], labels=None, autopct="%1.1f%%")
        plt.legend(
            data["name"],
            loc="upper right",
            bbox_to_anchor=(1.0, 1.0),
            fontsize=12,
        )
    elif chart_type == "#3":
        # Line Chart
        plt.title("Cooking Time by Recipe", fontsize=20)
        x_values = data["name"].to_numpy()  # Convert to numpy array
        y_values = data["cooking_time"].to_numpy()  # Convert to numpy array
        plt.plot(x_values, y_values)
        plt.xlabel("Recipes", fontsize=16)
        plt.ylabel("Cooking Time (min)", fontsize=16)
    else:
        print("Unknown chart type.")

    plt.tight_layout(pad=3.0)

    # Convert the plot to an image
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode("utf-8")

    return chart_image

class RecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes_list.html"
    context_object_name = "recipes"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        recipe_name = self.request.GET.get("Recipe_Name")
        ingredients = self.request.GET.getlist("Ingredients")
        selected_ingredient = self.request.GET.get("selected_ingredient")

        if recipe_name:
            queryset = queryset.filter(name__icontains=recipe_name)

        if ingredients:
            ingredient_query = Q()
            for ingredient_id in ingredients:
                ingredient_query |= Q(ingredients__id=ingredient_id)
            queryset = queryset.filter(ingredient_query)

        # Include selected ingredient in the filter
        if selected_ingredient:
            queryset = queryset.filter(ingredients__id=selected_ingredient)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Convert the QuerySet to a pandas DataFrame
            df = pd.DataFrame.from_records(context["recipes"].values())
            context["recipes_df"] = df

            context["form"] = RecipeSearchForm(self.request.GET)

            # Generate and pass the chart paths to the context
            chart_type = self.request.GET.get("chart_type")
            if chart_type:
                chart_data = {"name": df["name"], "cooking_time": df["cooking_time"]}
                if chart_type == "#1":
                    chart_data["labels"] = df["name"]
                elif chart_type == "#2":
                    chart_data["labels"] = df["name"]
                else:
                    chart_data["labels"] = None

                chart_image = get_chart(chart_type, chart_data)
                context["chart_image"] = chart_image

        except KeyError:
            # If KeyError occurs, handle the error and set the appropriate context variables
            context["recipes"] = []  # Set an empty list to recipes
            context[
                "error_message"
            ] = "There are no recipes with that combination of ingredients."

        return context


@login_required
def export_recipes_csv(request):
    # Get the filter parameters from the request
    recipe_name = request.GET.get("Recipe_Name")
    ingredients = request.GET.getlist("Ingredients")

    # Filter the Recipe objects based on the request parameters
    queryset = Recipe.objects.all()

    if recipe_name:
        queryset = queryset.filter(name__icontains=recipe_name)

    if ingredients:
        for ingredient in ingredients:
            # Check if the ingredient parameter is empty
            if ingredient:
                queryset = queryset.filter(ingredients__id=ingredient)

    # Convert the filtered QuerySet to a list of dictionaries
    recipe_data = list(queryset.values())

    # Get the related Ingredient data for each recipe
    for data in recipe_data:
        recipe = Recipe.objects.get(pk=data["id"])
        data["ingredients"] = ", ".join(
            [ingredient.name for ingredient in recipe.ingredients.all()]
        )

    # Create the DataFrame from the list of dictionaries
    df = pd.DataFrame.from_records(recipe_data)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="recipes.csv"'
    df.to_csv(path_or_buf=response, index=False)
    return response


@login_required
def generate_chart(request):
    chart_type = request.GET.get("chart_type")
    recipe_name = request.GET.get("Recipe_Name")
    ingredients = request.GET.getlist("Ingredients")

    # Filter the Recipe objects based on the request parameters
    queryset = Recipe.objects.all()

    if recipe_name:
        queryset = queryset.filter(name__icontains=recipe_name)

    if ingredients:
        for ingredient in ingredients:
            # Check if the ingredient parameter is empty
            if ingredient:
                queryset = queryset.filter(ingredients__id=ingredient)

    # Convert the filtered QuerySet to a list of dictionaries
    recipe_data = list(queryset.values())

    # Get the related Ingredient data for each recipe
    for data in recipe_data:
        recipe = Recipe.objects.get(pk=data["id"])
        data["ingredients"] = ", ".join(
            [ingredient.name for ingredient in recipe.ingredients.all()]
        )

    # Create the DataFrame from the list of dictionaries
    df = pd.DataFrame.from_records(recipe_data)

    chart_data = {"name": df["name"], "cooking_time": df["cooking_time"]}
    if chart_type == "#1":
        chart_data["labels"] = df["name"]
    elif chart_type == "#2":
        # For Pie Chart, labels should be the recipe names, and not the cooking times
        chart_data["labels"] = df["name"]
    else:
        chart_data["labels"] = None

    chart_image = get_chart(chart_type, chart_data)
    return JsonResponse({"chart_image": chart_image})


@login_required
def about_page(request):
    return render(request, "recipes/about.html")


class RecipesDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/details.html"
    context_object_name = "recipe"


logger = logging.getLogger(__name__)

@login_required
def add_recipe(request):
    IngredientFormSet = formset_factory(NewIngredientForm, extra=1, max_num=5)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                recipe = form.save(commit=False)

                selected_ingredients_count = len(form.cleaned_data["ingredients"])
                new_ingredients_count = sum(
                    1
                    for ingredient_form in formset
                    if ingredient_form.cleaned_data.get("new_ingredient")
                )
                total_ingredients = selected_ingredients_count + new_ingredients_count

                if recipe.cooking_time < 10 and total_ingredients < 4:
                    recipe.difficulty = "Easy"
                elif recipe.cooking_time < 10 and total_ingredients >= 4:
                    recipe.difficulty = "Medium"
                elif recipe.cooking_time >= 10 and total_ingredients < 4:
                    recipe.difficulty = "Intermediate"
                else:
                    recipe.difficulty = "Hard"

                recipe.save()
                form.save_m2m()

                for ingredient_form in formset:
                    new_ingredient_name = ingredient_form.cleaned_data.get("new_ingredient")
                    print(f"New Ingredient Name: {new_ingredient_name}")
                    if new_ingredient_name:
                        ingredient, created = Ingredient.objects.get_or_create(name=new_ingredient_name)
                        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

                messages.success(request, "Recipe added successfully.")

                if "save_and_add" in request.POST:
                    return redirect("recipes:add_recipe")

                return redirect(recipe)

            except Exception as e:
                # Log detailed error information
                logger.error("Error while saving recipe for user %s: %s", request.user.username, str(e))
                messages.error(request, "Error while saving recipe. Please try again.")

        else:
            # Log form and formset errors for debugging
            logger.error("Form errors: %s", form.errors)
            for i, form in enumerate(formset):
                logger.error("Formset form %d errors: %s", i + 1, form.errors)
            messages.error(request, "Form validation failed. Please check the entered data.")

    else:
        form = RecipeForm()
        form.fields["ingredients"].queryset = Ingredient.objects.order_by("name")
        formset = IngredientFormSet()

    context = {"form": form, "formset": formset}
    return render(request, "recipes/add_recipe.html", context)