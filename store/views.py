import random
import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from user.utils       import login_check, generate_token
from .models          import Product, Brand
from order.models     import Review

class ProductListView(View):
    def get(self, request):
        brands     = request.GET.getlist('brand')
        types      = request.GET.getlist('type')
        search     = request.GET.get('search')
        min_price  = request.GET.get('min_price')
        max_price  = request.GET.get('max_price')
        page       = int(request.GET.get('page', 1))

        q = Q()

        if brands:
            q &= Q(brand__name__in=brands)

        if types:
            q &= Q(product_type__name__in=types)

        if min_price and max_price:
            q &= Q(market_price__range=(min_price,max_price))

        if search:
            q &= Q(brand__name__icontains=search) | Q(product_type__name__icontains=search) | Q(title__icontains=search)

        products_list = Product.objects.select_related('product_type').prefetch_related('brand__product_set').filter(q)

        page_size = 21
        limit     = page * page_size
        offset    = limit - page_size
        products  = products_list[offset:limit]

        result = []

        for product in products:
            result.append({
                'name'         : product.title,
                'brand'        : product.brand.name,
                'price'        : product.market_price,
                'sale_price'   : product.sale_price,
                'description'  : product.description,
                'gender'       : product.gender.name,
                'type'         : product.product_type.name,
                'image'        : product.thumnail_url,
                'count'        : product.brand.product_set.all().count(),
                'heartCount'   : random.randint(50,200),
                'commentCount' : random.randint(50,166)
            })

        return JsonResponse({'result': result}, status=200)

class ProductDetailsView(View):
    def get(self,request,product_id):
        result = []
        try:
            product    = Product.objects.prefetch_related('productimage_set').filter(id=product_id)

            if not product:
                return JsonResponse({"message":"NOT_EXIST"}, status=400)

            product_info   = product.get()
            # imgs = product_info.productimage_set.all() 
            result.append({
                'detail_image' : [{
                    'image_url' : image.image_url
                }for image in product_info.productimage_set.all()],
                'id'           : product_info.id,
                'title'        : product_info.title,
                'market_price' : product_info.market_price,
                'sale_price'   : product_info.sale_price,
                'description'  : product_info.description,
                'product_img'  : product_info.thumnail_url,

            })
            return JsonResponse({'result': result}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status=400)

class Reviews(View):
    @login_check
    def post(self,request,product_id):
        try:
            data = json.loads(request.body)
            user = request.user
            Review.objects.create(
                content          = data['content'],
                rate             = data['rate'],
                review_image_url = data['review_image_url'],
                user             = user,
                product_id       = product_id
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)

    def get(self,request,product_id):
        try:
            page      = int(request.GET.get('page', 1))
            page_size = 5
            limit     = page * page_size
            offset    = limit - page_size

            reviews_list = Review.objects.order_by('-id').select_related('product','user').filter(product_id=product_id)
            reviews      = reviews_list[offset:limit]

            result = [{
                'id'         : review.id,
                'title'      : review.product.title,
                'content'    : review.content,
                'user'       : review.user.email.split('@')[0],
                'image'      : review.review_image_url,
                'rate'       : review.rate,
                'date'       : review.created_at

            } for review in reviews]

            return JsonResponse({
                'message' : 'SUCCESS',
                'review_list' : result,
                'total_count' : reviews_list.count()
            },status =200)

        except Exception as ex:
            return JsonResponse({'message':'ERROR_' + ex.args[0]}, status = 400)

    @login_check
    def delete(self,request,product_id):
        try:
            data = json.loads(request.body)
            user = request.user

            del_reivew = Review.objects.filter(id=data['review_id'],user=user )

            if not del_reivew.exists():
                return JsonResponse({'message' : 'INVAILD_REVIEW'}, status = 400)

            review = Review.objects.get(id=data['review_id'])
            review.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status = 204)

        except KeyError as ex:
            return JsonResponse({'message' : 'KEY_ERROR_' + ex.args[0]}, status = 400)
        except Exception as ex:
            return JsonResponse({'message' : 'ERROR_' + ex.args[0]}, status = 400)
