from django.db import models

# Create your models here.
class Roles(models.Model):
    role = models.CharField(max_length=50, unique=True)

class Users(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    date = models.DateTimeField
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

#  #veg/non veg etc
class FoodTypes(models.Model):   #ADMIN
    foodtype = models.CharField(max_length=200, unique=True)
    # imguid = models.CharField(max_length=255)
    uuid = models.CharField(max_length=200)

#
# #italian/bbq/fast food etc
class Categories(models.Model):  #ADMIN
    category = models.CharField(max_length=200, unique=True)
    img = models.ImageField(upload_to='images/', default=None)



class Books(models.Model): #ADMIN
    book_name = models.CharField(max_length=200, unique=True)
    book_author = models.CharField(max_length=200)
    book_cover = models.ImageField(upload_to='books/', default=None)
    book = models.FileField(upload_to='books/',default=None)
    uuid = models.CharField(max_length=255)
    # book pdf field....?????????????

# class Resturants(models.Model):  #RESTURANT OWNER
#     name = models.CharField(max_length=200)
#     location = models.CharField(max_length=255)
#     contact = models.CharField(max_length=11)
#     # image = models.ImageField
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE)
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#
# class ResturantRatings(models.Model):
#     resturant = models.ForeignKey(Resturants, on_delete=models.CASCADE)
#     person_name = models.CharField(max_length=255)
#     person_email = models.CharField(max_length=255)
#     review = models.CharField(max_length=255)
#     ratings = models.IntegerField
#     date = models.DateField
#     time = models.TimeField
#
#
#
# # pizza/drinks/sandwiches/burgers
# class Menu(models.Model): # RESTURANT OWNER
#     resturant = models.ForeignKey(Resturants, on_delete=models.CASCADE)
#     menu_name = models.CharField(max_length=200, unique=True)
#
# #RESTUTANT OWNER
# class Dishes(models.Model):
#     foodName = models.CharField(max_length=200)
#     food_details = models.CharField(max_length=255)
#     food_price = models.CharField(max_length=15)
#     #food_price = models.DecimalField(max_digits = 15, decimal_places = 2,)
#     # food_image = models.ImageField
#     date = models.DateTimeField
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     foodtype = models.ForeignKey(FoodTypes, on_delete=models.CASCADE)
#     resturant = models.ForeignKey(Resturants, on_delete=models.CASCADE)
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE)
#
# class DishReview(models.Model):
#     dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
#     person_name = models.CharField(max_length=255)
#     person_email = models.CharField(max_length=255)
#     date = models.DateTimeField
#     review = models.CharField(max_length=255)
#     ratings = models.IntegerField
#
#
# class MenuCards(models.Model): #RESTURANT OWNER
#     resturant = models.ForeignKey(Resturants, on_delete=models.CASCADE)
#     card = models.ImageField
#
# class Videos(models.Model): #RESTURANT OWNER
#     resturant = models.ForeignKey(Resturants, on_delete=models.CASCADE)
#     videos = models.CharField(max_length=255)   #field..........??????????????????
#
#
# class Coupens(models.Model):  # RESTURANT OWNER
#     resturant = models.ForeignKey(Resturants, on_delete=models.CASCADE)
#     coupen_code = models.CharField(max_length=5, unique=True)
#     discount = models.IntegerField
#
# # class Cart(models.Model): #Customer
# #     dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
# #     user = models.ForeignKey(Users, on_delete=models.CASCADE)
# #     resturant = models.ForeignKey(Resturants, on_delete=models.CASCADE)
# #     quantity = models.IntegerField
#
# class Orders(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
#     customer_name = models.CharField(max_length=255)
#     customer_address = models.CharField(max_length=255)
#     customer_phone = models.CharField(max_length=11)
#     address_type = models.CharField(max_length=200)
#     zipcode = models.CharField(max_length=11)
#     total = models.CharField(max_length=200)
#
#
# # class CompletedOrders(models.Model):
# #     pass
#
# class Feedback(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     feedback = models.CharField(max_length=500)
#     ratings = models.IntegerField





