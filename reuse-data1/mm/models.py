from django.db import models


class RawMaterialMovement(models.Model):
    rName = models.CharField(max_length=128)
    rDate = models.DateField()
    rMode = models.CharField(max_length=128)
    rTrips = models.CharField(max_length=128)
    rOrigin = models.CharField(max_length=128)
    rOriginLocation = models.CharField(max_length=128)
    rDestination = models.CharField(max_length=128)
    rDestinationLocation = models.CharField(max_length=128)
    rMaterial = models.CharField(max_length=2048)
    rHidden = models.CharField(max_length=1024)
    rTimestamp = models.CharField(max_length=128)

    def __str__(self):
        return str(self.rTimestamp)

    def __all__(self):
        return {
            'rName' : self.rName,
            'rDate' : self.rDate,
            'rTrips' : self.rTrips,
            'rMode' : self.rMode,
            'rOrigin' : self.rOrigin,
            'rOriginLocation' : self.rOriginLocation,
            'rDestination' : self.rDestination,
            'rDestinationLocation' : self.rDestinationLocation,
            'rMaterial' : self.rMaterial,
            'rHidden' : self.rHidden,
            'rTimestamp' : self.rTimestamp,
            }

class ExpandedMaterialMovement(models.Model):
        eName = models.CharField(max_length=128)
        eDate = models.DateField()
        eMode = models.CharField(max_length=128)
        eTrips = models.CharField(max_length=128)
        eOrigin = models.CharField(max_length=128)
        eOriginLocation = models.CharField(max_length=128)
        eDestination = models.CharField(max_length=128)
        eDestinationLocation = models.CharField(max_length=128)
        eTimestamp = models.CharField(max_length=128)
        eMaterial = models.CharField(max_length=128)
        ePallets = models.DecimalField(max_digits=8,decimal_places=2, default='0.00')
        # ePalletsX = models.CharField(max_length=128)
        eTripID = models.CharField(max_length=128)

        # REMOVED rMaterial :)
        # REMOVED rHidden :)
        # ADDED : ePallets + eMaterial + eTripID(SHA256 HASH)





###################################################
#  2021 UPGRADE
###################################################

# First : The locations table

# Second : The simple movement table


class Movement(models.Model):
    location_choices = [('I','IRC'),('T','TRMC'),('7','700'),('D','DOT')]  # COPIED + HARCODED FROM PRICING
    type_choices = [('D','Donations'),('O','Overflow'),('P','Processing'),('S','Salesfloor')]

    origin_type = models.CharField(max_length=1, choices=type_choices)
    origin_location = models.CharField(max_length=1, choices=location_choices)
    destination_type = models.CharField(max_length=1, choices=type_choices)
    destination_location = models.CharField(max_length=1, choices=location_choices)

    staff_id = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)


class Pallet(models.Model):
    movement = models.ForeignKey(Movement, on_delete=models.PROTECT)
    product_type = models.ForeignKey('pricing.ProductType', on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=5,decimal_places=2)
