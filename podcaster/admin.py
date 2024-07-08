from django.contrib import admin

from .models import Podcaster

# Register your models here.


class PodcasterAdmin(admin.ModelAdmin):
    list_display = ("name", "presentation")
    search_fields = ("name", "presentation")
    list_filter = ("name", "presentation")


admin.site.register(Podcaster, PodcasterAdmin)
