from django.db import models

# ------------------------------------
class DiegoStoreManager(models.Manager):
    def get_queryset(self):
        return super(DiegoStoreManager,self).get_queryset().filter(city='Diego')

class BostonStoreManager(models.Manager):
    def get_queryset(self):
        return super(DiegoStoreManager,self).get_queryset().filter(city='Boston')

class Store(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    
    objects=models.Manager()
    sandiego=DiegoStoreManager()
    boston=BostonStoreManager()
    
    class Meta:
        default_manager_name='objects'
        
#call 
Store.objects.all()
Store.sandiego.all()
Store.boston.all()



# ------------------------------------

class StoreQuerySet(models.QuerySet):
    def sandiego(self):
        return self.filter(city='Diego')
    
    def boston(self):
        return self.filter(city='Boston')
    
class Store(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    
    objects=models.Manager()
    shops=StoreQuerySet.as_manager()
    
    class Meta:
        default_manager_name='objects'

#call 
Store.objects.all()
Store.shops.all()
Store.shops.sandiego()
Store.shops.boston()
