# Generated by Django 3.0.3 on 2021-12-22 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vid', '0002_allnty'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountyMetrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('county', models.CharField(max_length=128)),
                ('state', models.CharField(max_length=128)),
                ('fips', models.CharField(max_length=128, null=True)),
                ('cases', models.IntegerField(null=True)),
                ('deaths', models.IntegerField(null=True)),
                ('population', models.IntegerField()),
                ('testPositivityRatio', models.FloatField(null=True)),
                ('infectionRate', models.FloatField(null=True)),
            ],
            options={
                'unique_together': {('date', 'fips')},
            },
        ),
        migrations.RenameModel(
            old_name='AllNTY',
            new_name='EntireUS',
        ),
        migrations.DeleteModel(
            name='CasesDeathsNTY',
        ),
        migrations.DeleteModel(
            name='MetricsActNow',
        ),
        migrations.DeleteModel(
            name='PennCases',
        ),
        migrations.DeleteModel(
            name='PennDeaths',
        ),
        migrations.DeleteModel(
            name='PennHospitals',
        ),
        migrations.DeleteModel(
            name='Places',
        ),
    ]
