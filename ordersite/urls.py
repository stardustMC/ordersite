"""ordersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from web.views import account, customer, prior, charge, price, my_order, my_profile

urlpatterns = [
    path('home/', account.home, name='home'),
    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('denied/', account.denied, name='denied'),
    path('email_send/', account.email_send, name='email_send'),
    path('email_login/', account.email_login, name='email_login'),

    path('customer/', customer.customer, name='customer'),
    path('customer/add/', customer.customer_add, name='customer_add'),
    path('customer/edit/<int:pk>/', customer.customer_edit, name='customer_edit'),
    path('customer/delete/<int:pk>/', customer.customer_delete, name='customer_delete'),

    path('customer/charge/<int:pk>/add/', charge.customer_charge_add, name='customer_charge_add'),
    path('customer/charge/<int:pk>/', charge.customer_charge, name='customer_charge'),

    path('customer/prior/', prior.customer_prior, name='customer_prior'),
    path('customer/prior/add/', prior.prior_add, name='prior_add'),
    path('customer/prior/edit/<int:pk>/', prior.prior_edit, name='prior_edit'),
    path('customer/prior/delete/<int:pk>/', prior.prior_delete, name='prior_delete'),

    path('price/', price.price, name='price'),
    path('price/add/', price.price_add, name='price_add'),
    path('price/edit/<int:pk>/', price.price_edit, name='price_edit'),
    path('price/delete/<int:pk>/', price.price_delete, name='price_delete'),

    path('my_order/', my_order.my_order, name='my_order'),
    path('my_order/add/', my_order.my_order_add, name='my_order_add'),
    path('my_order/revoke/<int:pk>/', my_order.my_order_revoke, name='my_order_revoke'),

    path('my_profile/', my_profile.my_profile, name='my_profile'),
    path('my_profile/reset/', my_profile.my_reset_password, name='my_profile_reset'),
]
