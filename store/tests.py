import json, jwt, bcrypt

from django.test import TestCase,TransactionTestCase
from store.models import *
from user.models import *
from order.models import *

from django.db import connection
from django.test import Client
from my_settings import SECRET_KEY,ALGORITHM

class productdetailviewtest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create(
            email = 'test@naver.com',
            password = '12341234'
        )

        self.brand  = Brand.objects.create(
            name = 'Roman Ltd',
            free_delivery = 50000    
        )

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
            gender        = self.gender,
            id            = 11           
        )

        self.review = Review.objects.create(
            content='좋아요',
            rate = 4,
            review_image_url = '소헌을 말해봐',
            user = self.user,
            product_id = self.product.id,
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

    def test_product_detail_success(self):
        client = Client()
        response = client.get('/store/11',content_type='application/json',**self.header)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['result'][0]['id'],11)
    
    def test_review_create_success(self):
        client = Client()
        review = {
            'content'           : self.review.content,
            'rate'              : self.review.rate,
            'review_image_url'  : self.review.review_image_url,
            'user'              : self.user.id,
            'product_id'        : self.product.id
        }
        response = client.post('/store/11/review',json.dumps(review), content_type = 'application/json',**self.header)
        self.assertEqual(response.status_code, 200)

    def test_review_keyerror_exist(self):
        client = Client()
        review = {
            'content'    : self.review.content,
            'rate'       : self.review.rate,
            'url'        : self.review.review_image_url,
            'user'       : self.user.id,
            'product_id' : self.product.id
        }
        response = client.post('/store/11/review',json.dumps(review), content_type = 'application/json',**self.header)
        self.assertEqual(response.status_code, 400)

    def test_review_read_success(self):
        client = Client()
        response = client.get('/store/11/review',content_type='application/json',**self.header) 
        print(response)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['review_list'][0]['id'],5)


    

        


