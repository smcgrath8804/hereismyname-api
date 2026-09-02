from django.contrib import admin

from .models import LinkVisibilityRule, VisibilityRule


admin.site.register(VisibilityRule)
admin.site.register(LinkVisibilityRule)