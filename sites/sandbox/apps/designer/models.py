from django.db import models

class TshirtSKU(models.Model):
	id = models.AutoField(primary_key=True)
	sku = models.PositiveIntegerField()
