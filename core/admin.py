from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Researcher, Architecture, TrainModel, PerformanceMetric, Tag


class ResearcherAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Additional information', {
        'fields':('specialization',),
    }),
    )

admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(Architecture)
admin.site.register(TrainModel)
admin.site.register(PerformanceMetric)
admin.site.register(Tag)