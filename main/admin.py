from django.contrib import admin

# Register your models here.
from .models import account, spitt, image, accFollowing

admin.site.register(account)
admin.site.register(spitt)
admin.site.register(image)
admin.site.register(accFollowing)