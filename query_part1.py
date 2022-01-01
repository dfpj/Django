# ************************Single records ******************************

#Sample=>
from django.db import models
class Person(models.Model):
    name = models.CharField(max_length=20)
    family = models.CharField(max_length=20)

# -----------Create-----------------
#1. Save() => create and update
person1 = Person(name="tom",family="hardy")
person1.save() # create
person1.name='tomy'
person1.save() # update

#2. create() => just create
person2 = Person.objects.create(name="keanu",family="reeves")


# -----------Read------------------
#1. get()  and  get_or_create()
person1 = Person.objects.get(name='keanu')

#not exist in table =>
personx= Person.objects.get(name='xxx') # Error: person.DoseNotExist  
#slove 1:
from django.core.exceptions import ObjectDoesNotExist
try:
    personx= Person.objects.get(name='xxx')
except ObjectDoesNotExist :
    pass

# slove 2:
personx= Person.objects.get_or_create(name='xxx',family='yyy') # if not exist => create recod


# Error MultipleObjectsReturned => return multi records instead single record 



# -----------Update-----------------
#1 save() 

#2 update()   single or multi update records
Person.objects.filter(name='tomy').update(name='tom')

#3 update_or_create() if not exist for update > create record
Person.objects.filter(name='tomy').update_or_create(name='tomy',family='hard')
# update_or_create() : if return multi records instead single record => MultipleObjectsReturned



# -----------Delete-----------------
Person.objects.filter(name='tomy').delete() # delete one or many record matched





# ************************Multiple records******************************

# -----------Create-----------------
# bulk_create()
person1 = Person(name='name1',family='family1')
person2 = Person(name='name2',family='family2')
person3 = Person(name='name3',family='family3')

person_list =[person1,person2,person3]
Person.objects.bulk_create(person_list) # not support pre_save & post_save signals

# slove signal problem and speed 
from django.db import transaction
@transaction.atomic
def bulk_person_creator(persons):
    for person in persons:
        person.save()

bulk_person_creator(person_list)

# -----------Read-----------------

#1 all()
person_list= Person.objects.all() # return queryset

#2 filter()
person_list=Person.objects.filter(name='?') # return queryset

#3 exclude()  Records that do not match the query requirement
person_list=Person.objects.exclude(name='?') # return queryset

# View Raw Query SQL => object of all - filter - exclude
person_list.qyery #  # queryset.query

#4 in_bulk()
Person.objects.in_bulk(['name1','name2'],field_name='name') #return dictionary

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# QuerySet = > Lazy-Evalutaion (QuerySet is perfect thanks DSF)
from django.db import connections,reset_queries
reset_queries()#flush the history of previous queries

person_list= Person.objects.all()
print(connections['default'].queries) # result=> []

#When to make a real contact with the database:
#1 for loop
for person in Person.objects.all():
    pass

#2 Slicing whit step argument
Person.objects.all()[::step] # if not step => create another queryset

#3 pickling
import pickle
pickle.dumps(Person.objects.all())

#4 repr()
repr(Person.objects.all())

#5 len()
len(Person.objects.all())
#Use count()
Person.objects.all().count()

#6 list()
list(Person.objects.all())

#7 bool() , or, and, if statemnet
if Person.objects.filter(name='?'):
    pass
#Use exists()
Person.objects.filter(name='?').exists()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# read records but not all coulmns . select favorite columns 
result = Person.objects.all()   #all() filter() exclude()
#1 only(favorite columns)
result.only('name') # return <QuerySet [<Person: name1>,...]>

#2 defer(unfavorite columns)
result.defer('family')# return <QuerySet [<Person: name1>,...]> not exist column family
 
#3 values(favorite columns)
result.values('name') # return <QuerySet [{'name': 'tom'}]>

#4 values_list(favorite columns)
result.values_list('name') # return <QuerySet [('tom',)]>


# check favoite columns in result
result.query.get_loaded_field_names() #{<class 'appname.models.Person'>: {'id', 'name'}}

# check unfavoite columns in One of the items result
result[0].get_deferred_fields() #return set => {'family'}



# -----------Update-----------------
#1 update

#2 select_for_update() It must be done with transaction otherwise => Error TransactionManagmentError

person_list = Person.objects.filter(name='?').select_for_update().exclude(family='?') #combine

@transaction.atomic  #
def bulk_person_update(persons):
    for person in persons:
        #change person and update whit save()
        person.save()

bulk_person_update(person_list)


#-----------------------------------------------------------------------
