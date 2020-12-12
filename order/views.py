import json
from datetime import datetime

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from user.utils import login_check
from .models import Cart, Order, OrderStatus
from store.models import (
                            Product, 
                            Brand, 
                            Color, 
                            Size, 
                            ProductColor
                        )
from user.models import (
                          TimeStampModel,
                          User,
                        )

class CartListView(View):         
    @login_check
    def post(self, request):
        try:
            data = json.loads(request.body)
            user         = User.objects.get(id=request.user.id)
            product      = Product.objects.get(id=data['product_id'])
            quantity     = data['quantity']
            color_id     = data.get('color_id',None)
            size_id      = data.get('size_id',None)
            delivery_fee = Product.objects.get(id=data['product_id']).brand.free_delivery


            if quantity < 1:
                return JsonResponse({'messagge':'INVALID_QUANTITY'},status=400)
            
            # order 생성
            order = Order.objects.filter(user_id=request.user.id,status_id=1)
            if not order.exists():
                created_order = Order.objects.create(
                    user_id   = request.user.id,
                    status_id = 1   
                )
                created_order.save()            
            current_order = order.last()
            
            # cart 수량 변경             
            cart = Cart.objects.filter(
                product    = product,
                order      = current_order,
                color_id   = color_id,
                size_id    = size_id
            )
            if cart.exists():
                for update_cart in cart:
                    update_cart.quantity = quantity
                    update_cart.save()
            else:
                Cart.objects.create(
                product    = product,
                order      = current_order,
                quantity   = quantity,
                color_id   = color_id,
                size_id    = size_id
            )

            return JsonResponse({'message':'SUCCESS'},status=201)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'INVALID_PRODUCT'},status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'},status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'},status=400)
    
    @login_check
    def get(self,request):
        try:
            order = Order.objects.prefetch_related('cart_set','cart_set__product').get(user_id=request.user,status=1)
            carts = order.cart_set.all()

            cartlist_data = [{
                "title"        : cart.product.title,
                "quantity"     : cart.quantity,
                "color"        : cart.color,
                "size"         : cart.size,
                "market_price" : cart.product.market_price,
                "sale_price"   : cart.product.sale_price, 
                "thumnail_url" : cart.product.thumnail_url,
                "delivery_fee" : cart.product.brand.free_delivery
            } for cart in carts]
        
            return JsonResponse({'message':cartlist_data},status=200)
    
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'INVALID_PRODUCT'},status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'},status=400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'},status=400)

class CartUpdateView(View):
    @login_check
    def delete(self,request):
        try:
            data = json.loads(request.body)
            user = request.user
            order_id = Order.objects.get(user=request.user,status_id=1).id
            del_product = Product.objects.get(id=data['product_id']).id
            in_cart = Cart.objects.get(product_id=del_product)
            in_cart.delete()
             
            return JsonResponse({'message':'SUCCESS'},status=201)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message':'INVALID_PRODUCT'},status=400)
