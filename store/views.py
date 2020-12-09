from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import Product, Brand

class ProductListView(View):
    def get(self, request):
      
        stores  = request.GET.getlist('store')
        brands  = request.GET.getlist('brand')
        types   = request.GET.getlist('type')
        search  = request.GET.get('search')
        page    = int(request.GET.get('page', 1))
        
        q = Q()

        if stores:
            q &= Q(store__name__in=stores)

        if brands:
            q &= Q(brand__name__in=brands)

        if types:
            q &= Q(product_type__name__in=types)

        if search:
            q &= Q(brand__name__icontains=search) | Q(product_type__name__icontains=search) | Q(title__icontains=search)
        
        products_list = Product.objects.filter(q)
        
        page_size = 20
        limit     = page * page_size
        offset    = limit - page_size
        products  = products_list[offset:limit]

        if not page:
            return JsonResponse({'message': 'PAGE_ERROR'}, status=400)
        
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
