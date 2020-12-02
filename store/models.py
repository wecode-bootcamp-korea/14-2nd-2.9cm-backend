from django.db import models

from user.models import TimeStampModel

class Menu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'menus'

class Category(models.Model):
    name = models.CharField(max_length=100)
    menu = models.ManyToManyField('Menu', through='MenuCategory')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'

class MenuCategory(models.Model):
    menu     = models.ForeignKey('Menu', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'menu_categories'

class SubCategory(models.Model):
    name     = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_categories'

class ProductType(models.Model):
    name         = models.CharField(max_length=100)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_types'

class Brand(models.Model):
    name          = models.CharField(max_length=100)
    free_delivery = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    category      = models.ManyToManyField('Category', through='BrandCategory')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'

class BrandCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand    = models.ForeignKey('Brand', on_delete=models.CASCADE)

    class Meta:
        db_table = 'brand_categories'

class Gender(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genders'

class Product(models.Model):
    title        = models.CharField(max_length=200)
    market_price = models.DecimalField(max_digits=10, decimal_places=0)
    sale_price   = models.DecimalField(max_digits=10, decimal_places=0)
    description  = models.TextField()
    brand        = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    gender       = models.ForeignKey('Gender', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    image_url = models.URLField(max_length=1000)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class Enquiry(TimeStampModel):
    email      = models.EmailField()
    content    = models.TextField()
    is_private = models.BooleanField()
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'enquiries'

class Size(models.Model):
    name     = models.CharField(max_length=200)
    category = models.ManyToManyField('Category', through='CategorySize')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sizes'

class CategorySize(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    size     = models.ForeignKey('Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_sizes'

class Color(models.Model):
    name    = models.CharField(max_length=200)
    product = models.ManyToManyField('Product', through='ProductColor')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'colors'

class ProductColor(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_colors' 
