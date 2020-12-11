import json
import jwt
import bcrypt

from store.models import * 
from user.models import *
from.models import *

from django.db import connection
from django.test import TestCase, TransactionTestCase
from django.test import Client
from unittest.mock import patch,MagicMock
from my_settings import SECRET_KEY,ALGORITHM

class CartListViewTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create(
            email = 'test@naver.com',
            password = '12341234'
        )

        self.brand  = Brand.objects.create(
            name = 'Roman Ltd',
            free_delivery = 50000    
        )
        self.menu = Menu.objects.create(name='MEN')

        self.category = Category.objects.create(
            name='신발',
        )
        
        self.sub_category = SubCategory.objects.create(
            name = '스니커즈',
            category = self.category
        )

        self.product_type = ProductType.objects.create(
            name = '하이탑',
            sub_category = self.sub_category
        )

        self.gender = Gender.objects.create(name='MEN')

        self.product = Product.objects.create(
            title         = '[Roman Ltd] Robin Cross',
            brand         = self.brand,
            market_price  = 109000,
            sale_price    = 98100,
            description   = '안녕하세요',
            thumnail_url  = '1234',
            product_type  = self.product_type,
            gender       = self.gender,
            id            = 11
        )
        self.order_status = OrderStatus.objects.create(
            name='장바구니'
        )
        
        self.order = Order.objects.create(user=self.user,status=self.order_status)
        
        self.cart = Cart.objects.create(
            quantity = 2,
            color = None,
            size = None,
            product = self.product,
            order = self.order,
        )

        self.DUMMY_AUTH = jwt.encode(
            {'id':self.user.id},
            SECRET_KEY,
            algorithm = ALGORITHM
            ).decode('utf-8')
        
        self.header = {
            'HTTP_Authorization' : self.DUMMY_AUTH,
        }
    
    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate orders_status')
            cursor.execute('set foreign_key_checks=1')

    def test_cart_quantity_check(self):
        client = Client()
        cart = {
            'user'    : self.user.id,   
            'product' : self.product.id,
            'color_id': None, 
            'size_id' : None,    
            'order'   : self.order.id,    
            'delivery_fee' : self.product.brand.free_delivery,
            'quantity' : 0 
        }
        
        response = client.post('/order/cart',json.dumps(cart), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_cart_create(self):
        client = Client()
        cart = {
            'user'    : self.user.id,   
            'product_id' : self.product.id,
            'color_id': None, 
            'size_id' : None,    
            'order'   : self.order.id,    
            'delivery_fee' : self.product.brand.free_delivery,
            'quantity' : 1 
        }
        
        response = client.post('/order/cart',json.dumps(cart), content_type = 'application/json',**self.header)
        self.assertEqual(response.status_code, 201)

    def test_cart_user_exist(self):
        client = Client()
        
        auth = jwt.encode(
            {'id':User.objects.all().last().id + 1},
            SECRET_KEY,
            algorithm = ALGORITHM
            ).decode('utf-8')
        
        header = {
            'HTTP_Authorization' : auth,
        }
        cart = {  
            'product_id'   : self.product.id,
            'color_id'     : None, 
            'size_id'      : None,    
            'order'        : self.order.id,    
            'delivery_fee' : self.product.brand.free_delivery,
            'quantity'     : 2 
        }
        
        response = client.post('/order/cart',json.dumps(cart), content_type = 'application/json',**header)
        self.assertEqual(response.status_code, 400)

    def test_cart_product_exist(self):
        client = Client()
        cart = { 
            'user'         : self.user.id, 
            'product_id'   : Product.objects.all().last().id + 1,
            'color_id'     : None, 
            'size_id'      : None,    
            'order'        : self.order.id,    
            'delivery_fee' : self.product.brand.free_delivery,
            'quantity'     : 2 
        }
        
        response = client.post('/order/cart',json.dumps(cart), content_type = 'application/json',**self.header)
        self.assertEqual(response.status_code, 400)
    
    def test_cart_keyerror_exist(self):
        client = Client()
        carts =[]
        carts.append({ 
            'color_id'     : None, 
            'size_id'      : None,    
            'order'        : self.order.id,    
            'delivery_fee' : self.product.brand.free_delivery,
            'quantity'     : 2 
        })

        carts.append({ 
            'product_id'   : self.product.id,
            'delivery_fee' : self.product.brand.free_delivery,
            'order'        : self.order.id, 
        })

        for cart in carts:
            response = client.post('/order/cart',json.dumps(cart), content_type = 'application/json',**self.header)
            self.assertEqual(response.status_code, 400)
    
    def test_cart_list_get_success(self):
        client = Client()
        response = client.get('/order/cart',content_type='application/json',**self.header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'][0]['title'],'[Roman Ltd] Robin Cross')
