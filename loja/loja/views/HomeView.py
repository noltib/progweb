from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from loja.models import Produto, Favorito


def home_view(request):
    produto = request.GET.get("produto")
    produtos = Produto.objects.all()
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)

    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = list(
            Favorito.objects.filter(user=request.user).values_list('produto_id', flat=True)
        )

    context = {
        'produtos': produtos,
        'favoritos_ids': favoritos_ids,
    }
    return render(request, template_name='home/home.html', context=context, status=200)


@login_required
def favoritar_produto_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    favorito = Favorito.objects.filter(user=request.user, produto=produto).first()
    if favorito:
        favorito.delete()
    else:
        Favorito.objects.create(user=request.user, produto=produto)

    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@login_required
def list_favoritos_view(request):
    favoritos = Favorito.objects.filter(user=request.user).select_related('produto')
    produtos = [fav.produto for fav in favoritos]
    favoritos_ids = [fav.produto_id for fav in favoritos]
    context = {
        'produtos': produtos,
        'favoritos': favoritos,
        'favoritos_ids': favoritos_ids,
    }
    return render(request, template_name='produto/favoritos.html', context=context, status=200)