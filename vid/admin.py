from django.contrib import admin
from vid.models import (PennCases,
                        PennDeaths,
                        PennHospitals,
                        CasesDeathsNTY,
                        MetricsActNow)

admin.site.register(PennCases)
admin.site.register(PennDeaths)
admin.site.register(PennHospitals)
admin.site.register(CasesDeathsNTY)
admin.site.register(MetricsActNow)
