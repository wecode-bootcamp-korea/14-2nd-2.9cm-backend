from django.db import models

from user.models import TimeStampModel

class Review(TimeStampModel):
    content          = models.TextField()
    rate             = models.DecimalField(max_digits=2, decimal_places=0)
    review_image_url = models.URLField(max_length=1000)
    product          = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    user             = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class Order(TimeStampModel):
    address = models.CharField(max_length=1000)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    status  = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class Cart(TimeStampModel):
    quantity = models.IntegerField()
    product  = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    color    = models.ForeignKey('store.Color', on_delete=models.CASCADE)
    size     = models.ForeignKey('store.Size', on_delete=models.CASCADE)
    order    = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'

class OrderStatus(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'orders_status'
