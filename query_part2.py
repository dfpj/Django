# -----------------CRUD => OneToMany ---------------
from django.db import models
class Team(models.Model):
    name= models.CharField(max_length=50)
    
class Player(models.Model):
    name= models.CharField(max_length=50)
    team= models.ForeignKey('Team', on_delete=models.CASCADE)

#----Read
Player.objects.get(name='ronaldo').team.name
Player.objects.filter(team__name='real madrid') # name is for Team  and Drink is in Team
team_obj=Team.objects.get(name='real madrid')
team_obj.player_set.filter(name__startwith='ron')

#----Create
#1 create()
team_obj.player_set.create(name='***') # create player whit specified team
#2 add()
new_player=Player(name='new_player') # whitout team
team_obj.player_set.add(new_player)

#----Clear  field team in model Player must => null=True
#1 clear()
# All player table records that have this team are replaced by a null => The relationship is neutralized
team_obj.player_set.clear()

#2 remove()
# One player table record that have this team are replaced by a null => The relationship is neutralized
team_obj=Team.objects.get(name='???')
player_obj=Player.objects.get(name='???')
team_obj.player_set.remove(player_obj)

#----Set
# set()
#1 change team in table Player to another team
list_player=Player.objects.filter(name='???')
#2 favorite team object 
team_obj=Team.objects.get(name='???')
#3 replcae
team_obj.players.set(list_player)




# -----------------CRUD => ManyToMany ---------------
class Book(models.Model):
    name= models.CharField(max_length=50)

class Author(models.Model):
    name = models.CharField(max_length=50)
    books= models.ManyToManyField(Book,related_name='authors')

#----Read
Author.objects.get(name='').books.all()
Author.objects.get(name='').books.create(name='book name')
Author.objects.filter(books__id=1)
book_obj=Book.objects.get(name='??')
book_obj.author_set.all()
book_obj.author_set.count()
book_obj.author_set.filter(name__startwith='authorname...')

#---- create 
# create()
book_obj.author_set.create(name='author name')

# add()
author_obj=Author.objects.get(name='??')
author_obj.save()
book_obj.author_set.add(author_obj)

# remove() & set() & delete() same CRUDE in onetomany



# -----------------CRUD => OneToOne ---------------
#Using the Related Manager in this relation does not make sense
