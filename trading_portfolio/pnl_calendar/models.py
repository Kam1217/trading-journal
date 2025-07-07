from django.db import models

# Create your models here.

#Create a Trades model to hold required csv data
class Trades(models.Model):
    trade_id = models.CharField(primary_key=True)
    trade_date = models.DateTimeField()
    gross_pnl = models.FloatField()
    fee = models.FloatField()
    net_pnl = models.FloatField()