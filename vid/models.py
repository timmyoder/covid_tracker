from django.db import models


class CountyMetrics(models.Model):
    """Cases by date from NTY github CSV"""
    date = models.DateTimeField()
    county = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    fips = models.CharField(max_length=128, null=True)
    cases = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    population = models.IntegerField()
    testPositivityRatio = models.FloatField(null=True)
    infectionRate = models.FloatField(null=True)

    class Meta:
        unique_together = (("date", "fips"),)


class EntireUS(models.Model):
    """Cases by date from NTY for the entire US github CSV"""
    date = models.DateTimeField()
    cases = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
