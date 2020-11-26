from django.db import models


class Places(models.Model):
    fips = models.CharField(max_length=5,
                            primary_key=True)
    country = models.CharField(max_length=128),
    state = models.CharField(max_length=128),
    county = models.CharField(max_length=128),
    level= models.CharField(max_length=128),
    lat = models.FloatField()
    locationId = models.CharField(max_length=128),
    lon = models.FloatField(),
    population = models.IntegerField()


class PennCaseDataDOH(models.Model):
    county = models.CharField(max_length=128)
    date = models.DateTimeField()
    cases = models.IntegerField()
    cases_avg_new = models.FloatField()
    cases_cume = models.IntegerField()
    population = models.IntegerField()
    cases_rate = models.FloatField()
    cases_avg_new_rate = models.FloatField()
    cases_cume_rate = models.IntegerField()

    class Meta:
        unique_together = (("date", "county"),)

