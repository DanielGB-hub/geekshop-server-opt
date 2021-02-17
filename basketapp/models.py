from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property

#class BasketQuerySet(models.QuerySet): // первый метод

    #def delete(self, *args, **kwargs):
        #for object in self:
            #object.product.quantity += object.quantity
            #object.product.save()

        #super().delete()


class Basket(models.Model):
    #object = BasketQuerySet.as_manager() // первый метод

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket') #
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)
#    objects = models.Manager() # для работы object

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()


    def _get_product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity
    
    product_cost = property(_get_product_cost)
    
    
    def _get_total_quantity(self):
        "return total quantity for user"
        #_items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity
        
    total_quantity = property(_get_total_quantity)
    
    
    def _get_total_cost(self):
        "return total cost for user"
        #_items = Basket.objects.filter(user=self.user)
        _items = _items = self.get_items_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod  # тут непонятно, как работает. С этим методом и без него разницы нет, хотя, может кеш все портит
    def get_items(pk):
        return Basket.objects.filter(pk=pk).first()


    #@staticmethod
    #def get_items(user):
        #return Basket.objects.filter(user=user).order_by('product__category').select_related()


    @staticmethod
    def get_product(user, product):
        #return Basket.objects.filter(pk=pk).first()
        return Basket.object.filter(user=user, product=product)
        #return Basket.objects.filter

    #@classmethod
    #def get_products_quantity(cls, user):
        #basket_items = cls.get_items(user)
        #basket_items_dic = {}
        #[basket_items_dic.update({item.product: item.quantity}) for item in basket_items]

        #return basket_items_dic

    #total_cost = property(_get_total_cost)

    #def delete(self): # первый метод
        #self.product.quantity += self.quantity
        #self.product.save()
        #super().delete()
        #52:17