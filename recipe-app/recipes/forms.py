from django import forms
from recipes.models import Recipe
from ingredients.models import Ingredient

CHART_CHOICES = (
    ("#1", "Bar Chart"),
    ("#2", "Pie Chart"),
    ("#3", "Line Chart"),
)

class RecipeSearchForm(forms.Form):
    Recipe_Name = forms.CharField(
        required=False,
        max_length=100,
        label="Recipe Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter a Recipe Name"}
        ),
    )

    Ingredients = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Ingredient.objects.order_by('name'),
        label="Ingredients",
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Chart Type",
    )

    def clean(self):
        cleaned_data = super().clean()
        recipe_name = cleaned_data.get("Recipe_Name")
        ingredients = cleaned_data.get("Ingredients")

        if not recipe_name and not ingredients:
            raise forms.ValidationError("Please enter a recipe name or select ingredients.")
        return cleaned_data


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ["difficulty"]  # Exclude the 'difficulty' field from the form
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-item"}),
            "cooking_time": forms.NumberInput(attrs={"class": "form-item"}),
            "description": forms.Textarea(attrs={"class": "form-item"}),
            "ingredients": forms.SelectMultiple(
                attrs={
                    "class": "form-item",
                    "name": "Please select an item from the list. Hold CTRL to select multiple items",
                }
            ),
            "pic": forms.FileInput(attrs={"class": "form-item"}),
        }


class NewIngredientForm(forms.Form):
    new_ingredient = forms.CharField(
        max_length=255,
        required=False,
        help_text="Add a new ingredient",
        widget=forms.TextInput(attrs={"class": "form-item"}),
    )