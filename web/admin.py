
from web.models import *


from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()


UserAdmin.list_display = ('email', 'username', 'paid_points', 'new_points', 'is_active', 'date_joined', 'last_login', 'is_staff')


admin.site.register(User, UserAdmin)


class CategoryAdmin(admin.ModelAdmin):

    class Meta:
        model = Category


    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)

class ObjectAdmin(admin.ModelAdmin):

    class Meta:
        model = Object


    list_display = ('category','name','buy_link')


admin.site.register(Object, ObjectAdmin)

class FootprintAdmin(admin.ModelAdmin):

    class Meta:
        model = Footprint


    list_display = ('object','size','created_by', 'verified', 'verified_by')
    exclude = ('verified_by', )


    def save_model(self, request, obj, form, change):
        if 'verified'  in obj.changed_fields:
            obj.verified_by = request.user
            obj.save()


admin.site.register(Footprint, FootprintAdmin)

class PointsAdmin(admin.ModelAdmin):

    class Meta:
        model = Points


    list_display = ('user','object','pending', 'footprint','points')


admin.site.register(Points, PointsAdmin)
