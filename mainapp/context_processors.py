from basketapp.models import Basket

def basket(request):
   #print(f'context processor basket works')
   basket_items = []

   if request.user.is_authenticated:
       #basket_items = Basket.objects.filter(user=request.user) # оптимизация
       basket_items = request.user.basket.select_related()
       #basket_items = Basket.get_items(request.user)

   return {
       'basket': basket_items
   }
