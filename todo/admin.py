from django.contrib import admin
from .models import Todo


class admintodo(admin.ModelAdmin):
    readonly_fields = ('createdate',)


admin.site.register(Todo, admintodo)





