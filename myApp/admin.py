from django.contrib import admin
from myApp.models import *
# Register your models here.



class PostAdmin(admin.ModelAdmin):
    list_display = ['title','new_date','id',]


admin.site.register(Post,PostAdmin)
admin.site.register(UserSave)
admin.site.register(Sepet)
