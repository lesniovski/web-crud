from django.shortcuts import render
from .models import Produto
from django.http import Http404
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def get_produto():
    try:
        arrayProdutos = Produto.objects.all()
        return sorted(arrayProdutos, key = Produto.get_name)
    except:
        return None

@csrf_protect
def produto(request):
    token = request.META['CSRF_COOKIE']
    print("## Token ##: ", token)
    #list
    data = {}
    data['list'] = []
    data['error'] = []
    # New and Update
    if request.method == 'POST':
        id = int(request.POST.get('id', -1))
        cod = request.POST.get('cod')
        nome = request.POST.get('nome')
        unidMedida = request.POST.get('unidMedida')
        preco = request.POST.get('preco')
        try:
            if (id == -1):
                produto = Produto(cod=cod,nome=nome,unidMedida=unidMedida,preco=preco)
                produto.save()
            else:
                produto = Produto.objects.get(id=id)
                produto.cod = cod
                produto.nome = nome
                produto.unidMedida = unidMedida
                produto.preco = preco
                produto.save()
        except:
            data['error'].append("Erro ao cadastrar produto! ")
            return render(request, 'produtos.html', data)
        data['list'] = get_produto()
        return render(request, 'produtos.html', data)
    # delete and update
    elif request.method == 'GET':
        id = request.GET.get('id')
        op = request.GET.get('op')
        if(id != None and op != None):
            if (op == "del"):
                try:
                    produto = Produto.objects.get(id=id)
                    produto.delete()
                    data['list'] = get_produto()
                    return render(request, 'produtos.html', data)
                except:
                    data['error'].append("Erro ao deletar produto! ")
                    return render(request, 'produtos.html', data)
            elif(op == "update"):
                data['produto'] = []
                try:
                    data['produto'].append(Produto.objects.get(id=id))
                    data['list'] = get_produto()
                except:
                    data['error'].append("Erro ao carregar produtos! ")
                    return render(request, 'produtos.html', data)
                return render(request, 'produtos.html', data)
        else:
            data['list'] = get_produto()
            return render(request, 'produtos.html', data)