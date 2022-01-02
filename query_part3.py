from django.db import models

class Person(models.Model):
    name = Persons.CharField(max_length=20)
    created=Persons.DateTimeField()

    pass

# ---------------------`WHERE` in SQL statement
result =Person.objects.filter(name='x') 
# result.query => SELECT * FROM appname_person WHERE name='x'



# ---------------------`=` in SQL statement
#       `exact` is case-sensitive in get() or filter()
Person.objects.get(id__exact=1)
Person.objects.get(name__exact="MsAd") # ~ MsAd
#       `iexact` is case-insensitive in get() or filter()
Person.objects.get(name__exact="MsAd") # ~ msad or MSAD and ...



# ---------------------`!=` in SQL statement
# exclude() or Q
Person.objects.exclude(id=1)# return queryset that have not id==1
result =Person.objects.exclude(id=1,name='x')# return queryset that have not id=1 and have not name='x' 
# result.query => SELECT * FROM appname_person WHERE NOT (id=1 AND name='x')

result =Person.objects.exclude(id=1).exclude(name='x')# return queryset that have not id=1 and have not name='x' 
# result.query => SELECT * FROM appname_person WHERE NOT id=1 AND NOT name='x'

from django.db.models import Q
Person.objects.filter(~Q(id=1))# return queryset that have not id==1
# `~` = NOT



# ---------------------`AND` in SQL statement
# `,`
result =Person.objects.filter(id=1,name='x')
# result.query => SELECT * FROM appname_person WHERE id=1 AND name='x'

# Q => &
result =Person.objects.filter(Q(id=1) & ~Q(name='x'))
# result.query => SELECT * FROM appname_person WHERE id=1 AND NOT name='x'




# ---------------------`OR` in SQL statement
# Q => |
result =Person.objects.filter(Q(id=1) | ~Q(name='x'))
# result.query => SELECT * FROM appname_person WHERE id=1 OR NOT name='x'




# ---------------------`IS` in SQL statement ~IS NULL
result =Person.objects.filter(name__isnull=True)
#or
result =Person.objects.filter(name=None)
#result.query =>  SELECT * FROM appname_person WHERE name IS NULL

# ---------------------`IS NOT` in SQL statement ~IS NOT NULL
result =Person.objects.filter(name__isnull=False)
#result.query =>  SELECT * FROM appname_person WHERE name IS NOT NULL



# ---------------------`IN` in SQL statement
result =Person.objects.filter(id__in=[1,2,3])
#result.query =>  SELECT * FROM appname_person WHERE id IN (1,2,3)



# ---------------------`LIKE  ILIKE` in SQL statement
# contains
result =Person.objects.filter(name__contains='x')
#result.query =>  SELECT * FROM appname_person WHERE name LIKE %x%

# startswith
result =Person.objects.filter(name__startswith='x')
#result.query =>  SELECT * FROM appname_person WHERE name LIKE x%

# endswith
result =Person.objects.filter(name__endswith='x')
#result.query =>  SELECT * FROM appname_person WHERE name LIKE %x

# exact
result =Person.objects.filter(name__exact='x')
#result.query =>  SELECT * FROM appname_person WHERE name LIKE x

#LIKE case-sensitive =>contains,startswith,endswith,exact
#ILIKE case-insensitive =>icontains,istartswith,iendswith,iexact





# ---------------------`REGEXP` in SQL statement
# `regex` case-sensitive
# `iregex` case-insensitive
result =Person.objects.filter(name__regex=r'^(?)')
#result.query =>  SELECT * FROM appname_person WHERE name REGEXP ^(?) @@sqlite




# ---------------------`>  =>  <  =<` in SQL statement Numeric fields
Person.objects.filter(id_gt=5)
Person.objects.filter(id_gte=5)
Person.objects.filter(id_lt=5)
Person.objects.filter(id_lte=5)



# ---------------------`DATE` in SQL statement
import datetime
time1=datetime.datetime(2017, 1, 10)
time2=datetime.datetime(2020, 1, 10)
# range =>BETWEEN
result = Person.objects.filter(created__range(time1,time2))
#result.query => SELECT * FROM appname_person WHERE created BETWEEN dat1 AND date2


result = Person.objects.filter(created__date=time1)
#SELECT * FROM appname_person WHERE created = time1

result = Person.objects.filter(created__year=2020)
result = Person.objects.filter(created__month=1)
result = Person.objects.filter(created__day=10)
result = Person.objects.filter(created__week=4) # each year is 53 weeks
result = Person.objects.filter(created__week_day=2) #(1=sunday),...(7=saturday)

result = Person.objects.filter(created__time=time1.time)
result = Person.objects.filter(created__houre=10)
result = Person.objects.filter(created__minute=1)
result = Person.objects.filter(created__second=5)



# ---------------------`DISTINCT` in SQL statement
# Delete duplicate records
# distinct()
Person.objects.distinct() # == Person.objects.all() Because it is based on id and we do not have a duplicate id  id=>primarykey

# Delete duplicate record in favorite column
Person.objects.values('name').distinct()

#just in postgresql :
Person.objects.distinct('name')




# ---------------------`ORDER` in SQL statement
# order_by()
Person.objects.order_by('name','-created')

# reverse()
Person.objects.filter(name='x').reverse() # same reverse in python



# ---------------------`LIMIT` and  `OFFSET`  in SQL statement
#whit slicing
Person.objects.all()[:5]

# first() last()
Person.objects.filter(name='x').first()
Person.objects.order_by('name','-created').last()

#earliest() latest() for datetime 
#both method argument(*args:datetime) => no need order_by()
Person.objects.earliest('-created')
Person.objects.latest('created','anotherdatetime')
