from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import Product, Brand

class ProductListView(View):
    def get(self, request):

        stores = request.GET.getlist('store')
        brands = request.GET.getlist('brand')
        types  = request.GET.getlist('type')

        q = Q()

        if stores:
            q &= Q(store__name__in=stores)

        if brands:
            q &= Q(brand__name__in=brands)

        if types:
            q &= Q(product_type__name__in=types)
        
        products = Product.objects.filter(q)[:20]
        
        result = []

        for product in products:
            result.append({
                'title'        : product.title,
                'market_price' : product.market_price,
                'sale_price'   : product.sale_price,
                'description'  : product.description,
                'gender'       : product.gender.name,
                'product_type' : product.product_type.name,
                'product_img'  : product.thumnail_url            
            })
                
        return JsonResponse({'result': result}, status=200)
