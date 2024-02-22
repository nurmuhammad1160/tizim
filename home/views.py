
from django.shortcuts import render, redirect
from .forms import LoginForm, EditProductForm, createForm, CreateUserProfil
from .models import Product, UserProfile, Income
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
# Create your views here.



def barcha(request):
    product = Product.objects.all()
    return render(request, 'boshliq/barcha.html', {'product':product})

def statistica(request):
    product = Product.objects.all()
    return render(request, 'boshliq/statistica.html', {'product':product})

def deleteProduct(request, p_id):
    product = Product.objects.get(pk=p_id)
    product.delete()
    return redirect('barcha')

def editProduct(request, p_id):
    product = Product.objects.get(pk=p_id)
    form =EditProductForm(request.POST or None)
    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('barcha')

    else:
        form = EditProductForm(instance=product)
        
    return render(request, 'boshliq/editProduct.html', {'product':product,'form':form})

def createProduct(request):
    form = createForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('barcha')
        
    return render(request, 'boshliq/create.html',{'form':form})

def detailProduct(request, p_id):
    product = Product.objects.get(pk=p_id)
    return render(request, 'boshliq/view.html',{'product':product})

def login_user(request):
    if request.user.is_authenticated:
        return render(request, 'boshliq/boshliq.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        if request.method == 'GET':  
            return render(request, 'login.html')

def home(request):
    if request.user.is_authenticated:
        role = request.user.userprofile.role
        if role == 'boshliq':
            return render(request, 'boshliq/boshliq.html')
        if role == 'admin':
            return render(request, 'admin.html')
        if role == 'sotuvchi':
            return render(request, 'income/home.html')
    else:
        return redirect('login')
        
    form = LoginForm()
        # return render(request, 'login.html', {'form': form})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                print('login amalga oshirildi')
                return redirect('home')
            else:
                print('xato')
       
    return render(request,'login.html',{'form': form})
    

def sign_out(request):
    logout(request)
    return redirect('login')   

def productSearch(request):
    q = request.GET.get('q')
 

    if q:
        query = Product.objects.filter(name__icontains=q)
        query = [{'name': product.name, 'info':product.info, 'id': product.id, 'amount': product.amount, 'price': product.price, 'type': product.type.tipe, 'category':product.category.category, 'subcategory':product.subcategory.subcat} for product in query]
    else:
        query = None

    query = list(query)

    return JsonResponse(data=query, safe=False)



def register(request):
    if request.method == 'POST':
        form = CreateUserProfil(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            rating = form.cleaned_data['rating']
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user,role=role, rating=rating)
            return render(request, 'boshliq/boshliq.html')
        
    else:
        form = CreateUserProfil
        return render(request, 'register.html', {'form':form})



# Income bo'limi



def inhome(request):
    
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
