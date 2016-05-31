from django.contrib import admin

from .models import *


class ModelAdmin2(admin.ModelAdmin):
    fields = ['var1']


class ModelAdmin3(admin.ModelAdmin):
    fields = ['var2']
    fieldsets = (
        (None, {
            'fields': ('var1', 'var2')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('var3',),
        }),
    )


admin.site.register(TestModel0)
admin.site.register(TestModel1)
admin.site.register(TestModel2, ModelAdmin2)
admin.site.register(TestModel3, ModelAdmin3)
