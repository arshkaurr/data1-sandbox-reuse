from django.db import models

# Create your models here.
class Location(models.Model):
    location_choices = [('I','IRC'),('T','TRMC'),('7','700'),('X','ALL'),('D','DOT')]
    location = models.CharField(max_length=1, choices=location_choices, unique=True)
    text = models.TextField(default='')
    shopify_location_id = models.CharField(max_length=16)
    def __str__(self):
        return self.location

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return self.category

class ProductType(models.Model):
    product_type = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=3, default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    def __str__(self):
        return self.product_type

class Product(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    classifier_choices = [('U','Unit'),('W','White'),('Y','Yellow'),('R','Red'),('O','Orange'),('B','Blue'),('G','Green'),('L','Lavender')]
    classifier = models.CharField(max_length=1, choices = classifier_choices)
    shopify_handle = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=256, default='')
    visible = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    def __str__(self):############ DONT CHANGE - USED IN THE STR FOR BARCODE AI
        return self.title ############ DONT CHANGE - USED IN THE STR FOR BARCODE AI

class Variant(models.Model):   #PROXY FOR BARCODE / SKU (Can be referenced!)
    variant = models.CharField(max_length=16, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    title = models.CharField(max_length=256, default='')
    code = models.CharField(max_length=4, default='')
    visible = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.product} - {self.variant}'

class Pricing(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    staff_id = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    print = models.BooleanField(default=False)
    inventory = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    shopify_inventory = models.BooleanField(default=False)

    # IMPORTANT : NEED TO SORT OUT ISSUE WHERE STAFF DELES ITEM AFTER ADDED TO SHOPIFY INVENTORY
    # IF CONDITION FOR DELETION -> IF shopify_inventory = True, then REMOVE the appropriate quanity (-NEGETIVE)

    def __str__(self):
        return self.staff_id




class Link(models.Model):
    order = models.IntegerField()
    text = models.CharField(max_length=128)
    url = models.CharField(max_length=256)
    category_choices = [('Q', 'Quick Links'), ('A','Active Guides'), ('C','Communications'), ('E','External Resources')]
    category =  models.CharField(max_length=1, choices=category_choices)
    link_style = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.text} - {self.category}'
