from django.db import models

# Create your models here.

#Create a Trade model to hold required csv data
class Trade(models.Model):
    trade_id = models.CharField(primary_key=True)
    trade_date = models.DateTimeField()
    gross_pnl = models.FloatField()
    fee = models.FloatField()
    net_pnl = models.FloatField()