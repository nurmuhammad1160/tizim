from django.utils import timezone

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from home.models import Product, Income
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def base(request):
    role = Product.objects.get()
    return render(request, 'incame/base.html', {'role':role})

def home(request):
    
    return render(request,template_name ='income/home.html')

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = list(Product.objects.filter(name__icontains=query).values('name', 'id','amount'))
    return JsonResponse({'results': results})

def sellProduct(request):
    ids = request.GET.get('ids')
    ids = [int(id) for id in ids.split(',')]
    products = Product.objects.filter(id__in=ids)
    data = serializers.serialize('python', products)
    json_data = json.dumps(data)
   
    context = {'products': products, 'json_data':json_data}
    return render(request, template_name='income/sellProduct.html', context=context)


@csrf_exempt
def sotish(request):
    if request.method == 'POST':
        # Get the products data from the request
        products = json.loads(request.POST.get('products', '[]'))

        # Process the products data
        errors = []
        user_profile = request.user.userprofile
        for item in products:
            product_id = item['id']
            quantity = item['quantity']

            product = Product.objects.get(id=product_id)

            if product.amount < quantity:
                errors.append(f'Shu raqamdagi mahsulot qolmagan {product_id}')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            for item in products:
                product_id = item['id']
                quantity = item['quantity']
                product = Product.objects.get(id=product_id)
                income = Income(product=product, customer=user_profile, real_price=product.price,p_amount=quantity, time=timezone.now())
                income.save()
                product.amount -= quantity
                product.save()
        return redirect('myallProduct')
           
def delete_amount(request, product_id):
    Income = Income.objects.get(id=product_id)
    Income.delete()
    return redirect('homePage')
