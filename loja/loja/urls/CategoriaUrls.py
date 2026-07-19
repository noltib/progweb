from django.urls import path

from loja.views.CategoriaView import list_categoria_view, add_categoria_view, edit_categoria_view, delete_categoria_view

urlpatterns = [

    path("", list_categoria_view, name="categoria"),

    path("add/", add_categoria_view, name="categoria_add"),

    path("edit/<int:id>/", edit_categoria_view, name="categoria_edit"),

    path("delete/<int:id>/", delete_categoria_view, name="categoria_delete"),

]