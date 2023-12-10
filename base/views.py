from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json
from .models import *
import stripe
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
  products = Product.objects.all()
  customer = Customer.objects.get(user=request.user)
  order, created = Order.objects.get_or_create(customer=customer)

  context = {
    'products': products,
    'order': order,
  }
  return render(request, 'base/index.html', context)

def cart(request):
  
  customer = Customer.objects.get(user=request.user)

  order, created = Order.objects.get_or_create(customer=customer)
  items = order.orderitem_set.all()

  context = {
    'items': items,
    'order': order,
  }

  return render(request, 'base/cart.html', context)

def checkout(request):
  customer = Customer.objects.get(user=request.user)

  order, created = Order.objects.get_or_create(customer=customer)
  items = order.orderitem_set.all()

  context = {
    'items': items,
    'order': order,
  }

  return render(request, 'base/checkout.html', context)

  
def updateOrder(request):

  data = json.loads(request.body)
  productId = data['productId']
  action = data['action']

  customer = Customer.objects.get(user=request.user)

  product = Product.objects.get(id=productId)
  order, created = Order.objects.get_or_create(customer=customer)
  item_tuple = OrderItem.objects.get_or_create(order=order, product=product)
  item = item_tuple[0]

  if action == 'add':
    item.quantity += 1

  elif action == 'remove':
    item.quantity -= 1

  item.save()

  if action == 'cancel':
    item.delete()

  if item.quantity <= 0:
    item.delete()
    
  return JsonResponse('Cart Updated', safe=False)

def processOrder(request):
  data = json.loads(request.body)

  customer = Customer.objects.get(user=request.user)

  order, created = Order.objects.get_or_create(customer=customer)
  
  shipping_address = ShippingAddress.objects.create(
    customer = customer,
    order = order,
    first_name = customer.user.first_name,
    last_name = customer.user.last_name,
    phone = data['phone'],
    email_address = data['email'],
    country = data['country'],
    address= data['address'],
  )

  shipping_address.save()

  return JsonResponse('Order Processing', safe=False)

@csrf_exempt
def getStripeKey(request):
  if request.method == 'GET':
    stripe_api_key = settings.STRIPE_PUBLISHABLE_KEY
    publickey = {'publicKey': stripe_api_key}

    return JsonResponse(publickey, safe=False)

@csrf_exempt
def stripe_checkout_session(request):
  if request.method == 'GET':
    stripe.api_key = settings.STRIPE_SECRET_KEY
    domain_url = 'http://127.0.0.1:8000/'
    try:
      checkout_session = stripe.checkout.Session.create(
        success_url=domain_url + 'success/',
        cancel_url=domain_url + 'cancel/',
        payment_method_types=['card'],
        mode='payment',
        line_items=[
          {
          'price': 'price_1OK5cYL4dnedMSOxl6surECP',
          'quantity': 2,
          }
        ],
      )
      
      return JsonResponse({'sessionId': checkout_session['id']})
    
    except ValueError as e:
      return JsonResponse({'error': str(e)})
    
def success(request):
  return render(request, 'base/')