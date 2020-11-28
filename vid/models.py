from django.db import models


class Places(models.Model):
    fips = models.CharField(max_length=5,
                            primary_key=True)
    country = models.CharField(max_length=128),
    state = models.CharField(max_length=128),
    county = models.CharField(max_length=128),
    lat = models.FloatField()
    locationId = models.CharField(max_length=128),
    lon = models.FloatField(),
    population = models.IntegerField()


class PennCases(models.Model):
    """Table to store case data directly from PA's DOH API"""
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


class PennHospitals(models.Model):
    """Table to store hospital data directly from PA's DOH API"""

    county = models.CharField(max_length=128)
    date = models.DateTimeField()

    aii_avail = models.IntegerField()
    aii_total = models.IntegerField()
    icu_avail = models.IntegerField()
    icu_total = models.IntegerField()
    med_avail = models.IntegerField()
    med_total = models.IntegerField()
    covid_patients = models.IntegerField()
    aii_percent = models.FloatField()
    icu_percent = models.FloatField()
    med_percent = models.FloatField()

    class Meta:
        unique_together = (("date", "county"),)


class PennDeaths(models.Model):
    """Table to store death data directly from PA's DOH API"""
    county = models.CharField(max_length=128)
    date = models.DateTimeField()
    population = models.IntegerField()
    deaths = models.IntegerField()
    deaths_cume = models.IntegerField()
    deaths_rate = models.FloatField()
    deaths_cume_rate = models.FloatField()

    class Meta:
        unique_together = (("date", "county"),)


class CasesDeathsNTY(models.Model):
    """Cases by date from CovidActNow API where better sources DNE"""
    date = models.DateTimeField()
    county = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    fips = models.CharField(max_length=128, null=True)
    cases = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    confirmed_cases = models.IntegerField(null=True)
    confirmed_deaths = models.IntegerField(null=True)
    probable_cases = models.IntegerField(null=True)
    probable_deaths = models.IntegerField(null=True)

    class Meta:
        unique_together = (("date", "fips"),)


class MetricsActNow(models.Model):
    """Death by date from CovidActNow API where better sources DNE"""
    date = models.DateTimeField()
    county = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    fips = models.CharField(max_length=128)
    testPositivityRatio = models.FloatField()
    infectionRate = models.FloatField()

    class Meta:
        unique_together = (("date", "fips"),)

