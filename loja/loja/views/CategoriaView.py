from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Categoria

def list_categoria_view(request):
    categorias = Categoria.objects.all()

    context = {
        'categorias': categorias
    }

    return render(
        request,
        template_name='categoria/categoria.html',
        context=context,
        status=200
    )


def add_categoria_view(request):

    if request.method == "POST":

        Categoria.objects.create(
            Categoria=request.POST["Categoria"]
        )

        return redirect("/categoria/")

    return render(
        request,
        template_name='categoria/categoria-add.html',
        status=200
    )


def edit_categoria_view(request, id):

    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":

        categoria.Categoria = request.POST["Categoria"]

        categoria.save()

        return redirect("/categoria/")

    context = {
        'categoria': categoria
    }

    return render(
        request,
        template_name='categoria/categoria-edit.html',
        context=context,
        status=200
    )


def delete_categoria_view(request, id):

    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":

        categoria.delete()

        return redirect("/categoria/")

    context = {
        'categoria': categoria
    }

    return render(
        request,
        template_name='categoria/categoria-delete.html',
        context=context,
        status=200
    )