from django.contrib import admin
from .models import *
from . import models


# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Sell_post)
admin.site.register(Sell_Post_Category)

