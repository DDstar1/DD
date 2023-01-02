
from django.contrib import admin
from main.models import UserInfo, UserPoint
# Register your models here.



class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'graph')

class UserPointAdmin(admin.ModelAdmin):
    list_display = ('user','point')
 

    
admin.site.register(UserInfo, UserInfoAdmin)

admin.site.register(UserPoint, UserPointAdmin)