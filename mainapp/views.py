from django.shortcuts import render
from django.utils import timezone
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):

    context = {
        'title': 'geek shop',

        'date': timezone.now()

    }

    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):

    context = {

        'title': 'GeekShop - Категории',

        'categories': ProductCategory.objects.all()

    }


    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('price')
    else:
        products = Product.objects.all().order_by('price')
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context.update({'products': products_paginator})
    return render(request, 'mainapp/products.html', context)
