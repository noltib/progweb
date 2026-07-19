from django.shortcuts import render, redirect, get_object_or_404

from loja.models import Fabricante
from loja.forms.FabricanteForm import FabricanteForm


def list_fabricante_view(request):

    fabricantes = Fabricante.objects.all()

    context = {

        "fabricantes": fabricantes

    }

    return render(

        request,

        "fabricante/fabricante.html",

        context

    )


def add_fabricante_view(request):

    if request.method == "POST":

        fabricanteForm = FabricanteForm(request.POST)

        if fabricanteForm.is_valid():

            fabricanteForm.save()

            return redirect("/fabricante/")

    else:

        fabricanteForm = FabricanteForm()

    context = {

        "fabricanteForm": fabricanteForm

    }

    return render(

        request,

        "fabricante/fabricante-add.html",

        context

    )


def edit_fabricante_view(request, id):

    fabricante = get_object_or_404(

        Fabricante,

        id=id

    )

    if request.method == "POST":

        fabricanteForm = FabricanteForm(

            request.POST,

            instance=fabricante

        )

        if fabricanteForm.is_valid():

            fabricanteForm.save()

            return redirect("/fabricante/")

    else:

        fabricanteForm = FabricanteForm(

            instance=fabricante

        )

    context = {

        "fabricanteForm": fabricanteForm

    }

    return render(

        request,

        "fabricante/fabricante-edit.html",

        context

    )


def delete_fabricante_view(request, id):

    fabricante = get_object_or_404(

        Fabricante,

        id=id

    )

    if request.method == "POST":

        fabricante.delete()

        return redirect("/fabricante/")

    context = {

        "fabricante": fabricante

    }

    return render(

        request,

        "fabricante/fabricante-delete.html",

        context

    )