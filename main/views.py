from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.forms import ProductForm
from django.urls import reverse
from django.forms import ModelForm
from main.models import Product
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_product_json(request):
    product_item = Product.objects.filter(user = request.user)
    return HttpResponse(serializers.serialize('json', product_item))

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        user = request.user

        new_product = Product(name=name, price=price, description=description, user=user)
        new_product.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def get_product_ajax(request,product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        data = {
            'name': product.name,
            'price': product.price,
            'description': product.description,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def delete_product_ajax(request):
    if(request.method == 'POST'):
        try:
            data = json.load(request)
            id = data.get("id")
            product = Product.objects.get(pk = id)
            product.delete()
            response_data = {
                'status': 'success',
                'message' : 'Produk berhasil dihapus'
            }
            return JsonResponse(response_data)
        except Product.DoesNotExist:
            response_data = {
                'status': 'failed',
                'message' : 'Produk tidak ditemukan'
            }
            return JsonResponse(response_data)
@csrf_exempt
def edit_product_ajax(request):
    if(request.method == 'POST'):
        try:
            data = json.load(request)
            id = data.get("id")
            name = data.get("name")
            price = data.get("price")
            description = data.get("description")
            product = Product.objects.get(pk = id)
            product.name = name
            product.description = description
            product.price = int(price)
            product.save()
            response_data = {
                'status': 'success',
                'message' : 'Produk berhasil diedit'
            }
            return JsonResponse(response_data)
        except Exception as e:
             response_data = {
                'status': 'failed',
                'message' : 'Terdapat kesalahan dalam mengedit produk: ' + str(e)
            }
             return JsonResponse(response_data)

@csrf_exempt
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        print("heheh not bad")
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'class': 'PBP D',
        'products':products,
        'last_login': request.COOKIES.get('last_login', 'Tidak ada data'),
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
@csrf_exempt
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
@csrf_exempt
def edit_product(request, id):
    # Get product berdasarkan ID
    product = Product.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'product': product}
    return render(request, "edit_product.html", context)

@csrf_exempt
def delete_product(request, id):
    # Get data berdasarkan ID
    product = Product.objects.get(pk = id)
    # Hapus data
    product.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@csrf_exempt
def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@csrf_exempt
def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_product = Product.objects.create(
            user = request.user,
            name = data["name"],
            price = int(data["price"]),
            description = data["description"]
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)