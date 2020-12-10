
import random

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import Product, Brand

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
