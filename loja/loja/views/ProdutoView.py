from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from loja.models import Categoria, Fabricante, Produto


def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {"produto": produto, "fabricantes": Fabricantes, "categorias": Categorias}
    return render(
        request, template_name="produto/produto-edit.html", context=context, status=200
    )


def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")

    produtos = Produto.objects.all()
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    if produto is not None:
        produtos = produtos.filter(Produto=produto)
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)

    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    if categoria is not None:
        produtos = produtos.filter(categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante=fabricante)
    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)
    if id is not None:
        produtos = produtos.filter(id=id)

    context = {"produtos": produtos}
    return render(
        request, template_name="produto/produto.html", context=context, status=200
    )


# adicione a função que trata o postback da interface de edição
def edit_produto_postback(request, id=None):
    # Processa o post back gerado pela action
    if request.method == "POST":
        # Salva dados editados
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")
        print("postback")
        print(id)
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            obj_produto.Produto = produto
            obj_produto.destaque = destaque is not None
            obj_produto.promocao = promocao is not None
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
            obj_produto.save()
            print("Produto %s salvo com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")


def details_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()
    context = {
        "produto": produto,
        "categorias": categorias,
        "fabricantes": fabricantes,
    }
    return render(
        request,
        template_name="produto/produto-details.html",
        context=context,
        status=200,
    )


def delete_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()
    context = {
        "produto": produto,
        "categorias": categorias,
        "fabricantes": fabricantes,
    }
    return render(
        request,
        template_name="produto/produto-delete.html",
        context=context,
        status=200,
    )


# adicione a função que trata o postback da interface de exclusão
def delete_produto_postback(request, id=None):
    if request.method == "POST":
        produto_id = request.POST.get("id")
        produto = Produto.objects.filter(id=produto_id).first()
        if produto is not None:
            if produto.image:
                fs = FileSystemStorage()
                try:
                    fs.delete(produto.image.name)
                except Exception:
                    pass
            produto.delete()
    return redirect("/produto")


def create_produto_view(request, id=None):
    if request.method == "POST":
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")

        try:
            obj_produto = Produto()
            obj_produto.Produto = produto
            obj_produto.destaque = destaque is not None
            obj_produto.promocao = promocao is not None
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
            obj_produto.preco = 0
            if (preco is not None) and (preco != ""):
                obj_produto.preco = preco
            if categoria is not None and categoria.isdigit() and int(categoria) > 0:
                obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            if fabricante is not None and fabricante.isdigit() and int(fabricante) > 0:
                obj_produto.fabricante = Fabricante.objects.filter(
                    id=fabricante
                ).first()
            obj_produto.criado_em = timezone.now()
            obj_produto.alterado_em = obj_produto.criado_em
            # Se for anexado arquivo, salva na pasta e guarda nome no objeto
            if request.FILES is not None:
                if "image" in request.FILES:
                    imagefile = request.FILES["image"]
                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)
                    if filename:
                        obj_produto.image = filename
            obj_produto.save()
        except Exception as e:
            print("Erro inserindo produto: %s" % e)
        return redirect("/produto")

    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()
    return render(
        request,
        template_name="produto/produto-create.html",
        context={"categorias": categorias, "fabricantes": fabricantes},
        status=200,
    )
