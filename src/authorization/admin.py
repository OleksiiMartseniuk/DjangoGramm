from django.contrib import admin

from .models import CustomUser, Contact

admin.site.register(CustomUser)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_from', 'user_to')
    list_filter = ('user_from', 'user_to')
