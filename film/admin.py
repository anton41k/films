from django.contrib import admin
from film.models import *


class ScreensInline(admin.TabularInline):
    model = Screens
    extra = 5

class FilmsAdmin(admin.ModelAdmin):
	list_display=('name','orig_name','poster','date_film')
	inlines = [ScreensInline,]



class ComentsAdmin(admin.ModelAdmin):
	list_display=('us','message','date_coment')
class ScreensAdmin(admin.ModelAdmin):
	list_display=('films','screen')
class RatingAdmin(admin.ModelAdmin):
	list_display=('film','user_rating','rating')

admin.site.register(Films,FilmsAdmin)
admin.site.register(Coments,ComentsAdmin)
admin.site.register(Genres)
admin.site.register(Screens,ScreensAdmin)
admin.site.register(AddUser)
admin.site.register(SmsUser)
admin.site.register(Rating,RatingAdmin)


