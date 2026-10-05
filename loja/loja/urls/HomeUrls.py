from django.urls import path
from loja.views.HomeView import home_view, favoritar_produto_view, list_favoritos_view

urlpatterns = [
    path("", home_view, name='home'),
    path("favoritos/", list_favoritos_view, name='favoritos'),
    path("favoritar/<int:produto_id>/", favoritar_produto_view, name='favoritar_produto'),
]
