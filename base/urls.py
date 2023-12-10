from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_order/', updateOrder, name='update_order'),
    path('process_order/', processOrder, name='process_order'),
    path('get_stripe_key/', getStripeKey),
    path('stripe_checkout/', stripe_checkout_session),
    path('success/', stripe_checkout_session),
    path('cancel/', stripe_checkout_session),
]