from django.urls import path

from loja.views.FabricanteView import add_fabricante_view, delete_fabricante_view, edit_fabricante_view, list_fabricante_view

urlpatterns = [

    path("", list_fabricante_view, name="fabricante"),

    path("add/", add_fabricante_view, name="fabricante_add"),

    path("edit/<int:id>/", edit_fabricante_view, name="fabricante_edit"),

    path("delete/<int:id>/", delete_fabricante_view, name="fabricante_delete"),

]