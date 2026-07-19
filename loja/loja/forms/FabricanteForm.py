from django import forms
from django.forms import ModelForm
from loja.models import Fabricante


class FabricanteForm(ModelForm):

    class Meta:

        model = Fabricante

        fields = "__all__"

        widgets = {

            "Fabricante": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),

        }