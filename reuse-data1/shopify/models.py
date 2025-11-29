from django.db import models


#NEED TO KILL THIS
# class AceInventory(models.Model):
#     Index = models.IntegerField(primary_key=True)
#     ItemCode = models.CharField(max_length=64)
#     Location = models.CharField(max_length=64)
#     Department = models.CharField(max_length=64)
#     Title = models.CharField(max_length=1024)
#     Upc = models.CharField(max_length=64)
#     Qoh = models.IntegerField()
#     Mpn = models.CharField(max_length=64)
#     Retail = models.DecimalField(max_digits=8, decimal_places=2)
#     Status = models.CharField(max_length=64)



class AceInventoryList(models.Model):
    Index = models.IntegerField(primary_key=True)
    ItemCode = models.CharField(max_length=64)
    Location = models.CharField(max_length=64)
    Department = models.CharField(max_length=64)
    Title = models.CharField(max_length=1024)
    Upc = models.CharField(max_length=64)
    Qoh = models.IntegerField()
    Mpn = models.CharField(max_length=64)
    Retail = models.DecimalField(max_digits=8, decimal_places=2)
    Status = models.CharField(max_length=64)



class InventoryMovement(models.Model):
    timestamp = models.DateTimeField()
    handle = models.CharField(max_length=128)
    barcode = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    option1 = models.CharField(max_length=128)
    product_id = models.CharField(max_length=128)
    variant_id = models.CharField(max_length=128)
    compare_at_price = models.DecimalField(max_digits=16, decimal_places=2)
    inventory_item_id = models.CharField(max_length=128)
    product_type = models.CharField(max_length=128)
    vendor = models.CharField(max_length=128)
    sku = models.CharField(max_length=128)

    staff = models.CharField(max_length=128)
    meta = models.TextField()
    location_id = models.CharField(max_length=128)
    quantity = models.IntegerField()

    def __str__(self):
        return self.barcode


class InventoryLookup(models.Model):
    timestamp = models.DateTimeField()
    handle = models.CharField(max_length=128)
    barcode = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    option1 = models.CharField(max_length=128)
    product_id = models.CharField(max_length=128)
    variant_id = models.CharField(max_length=128)
    compare_at_price = models.DecimalField(max_digits=16, decimal_places=2)
    inventory_item_id = models.CharField(max_length=128)
    product_type = models.CharField(max_length=128)
    vendor = models.CharField(max_length=128)
    sku = models.CharField(max_length=128)

    body_html = models.TextField(default='')

    def __str__(self):
        return self.barcode
